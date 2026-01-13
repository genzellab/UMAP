% delta_analysisPFC.m
% -------------------------------------------------------------------------
% Detect delta waves (1-6 Hz) in PFC LFP across pre/post sessions and save
% timestamps and waveform snippets for later analysis/visualization.
%
% Overview:
% - Traverses rat/session folders (getfolder / checksequence).
% - Loads sleep scoring (*states*.mat) and PFC LFP (*PFC*.mat) per session.
% - Selects epochs of the requested sleep stage (ss, default NREM = 3).
% - Breaks continuous recordings into 1-second epochs and groups contiguous
%   epochs of the requested stage into segments.
% - Bandpass filters each segment (1-6 Hz) and runs FindDeltaWaves on the
%   concatenated bandpassed data to detect delta events.
% - Extracts waveform snippets from both broadband and bandpassed signals.
% - Saves per-session and per-rat .mat files:
%     - delta_waveform_broadband_<session>.mat
%     - delta_waveform_broadband_visualization_<session>.mat
%     - delta_waveform_<session>.mat
%     - delta_timestamps_<session>.mat
%     - delta_count_<session>.mat
%     - delta_waveform_broadband_compilation_Rat<rat>.mat
%     - delta_waveform_compilation_Rat<rat>.mat
%
% Required helper functions / expectations:
% - getfolder (returns folder names in current directory)
% - checksequence (returns ordered session subfolders inside a sequence folder)
% - ConsecutiveOnes (given a binary vector returns lengths of consecutive 1s)
% - FindDeltaWaves (accepts [time, value] matrix and returns events matrix,
%   with at least start and end times, used as delta(:,1) and delta(:,3))
% - Input files in session folder:
%     * A "*states*.mat" file that defines 'states' vector (one value per second)
%     * A "*PFC*.mat" file that contains a variable named PFC (LFP vector)
%
% Notes / assumptions:
% - Sampling rate fn is set near top (default 2500 Hz here).
% - The script pads/truncates recordings to 45 minutes per chunk (45*60 sec).
% - Sessions with 'trial5' (post-trial 5) are handled as 4 consecutive 45-min
%   chunks and processed separately.
% - PFC signal is multiplied by 0.195 (calibration factor present in code).
% - NaNs in PFC and states are replaced with zeros before detection (this is
%   preserved as original behavior).
%
% Suggested future improvements (not implemented here):
% - Parameterize fn, stage selection, padding length, and scale factor.
% - Avoid replacing NaNs with zeros; instead skip NaN windows.
% - Factor repeated trial5 chunk processing into helper function.
%
% -------------------------------------------------------------------------
clear variables
clc
close all

% Add project/toolbox paths (adjust to your system if needed)
addpath(genpath('/home/genzel/Documents/CorticoHippocampal'))
addpath(genpath('/home/genzel/Documents/UMAP_Basic_OS/huseyin'))
addpath('/home/genzel/Documents/ADRITOOLS/')
cd('/media/genzel/genzel1/UMAP_Basic_OS')

% Sleep stage selection:
% The original script uses a fixed selection: ss = 3 (NREM).
% If you want interactive selection, you can re-enable the listdlg section.
ss = 3;               % 3 == NREM
fn = 2500;            % sampling frequency (Hz) for these data

% Initialize outputs / accumulators
total_delta = [];
total_delta_minute = [];
delta_total_data = {};
rat_folder = getfolder;   % custom helper that lists rat folders
% Note: rat_folder often includes helper directories; user trimmed in some versions

% Currently the script processes a single rat by setting k = 1.
% To process all rats: replace the next two lines by "for k = 1:length(rat_folder)"
k = 1;
cd(rat_folder{k})
g = getfolder;                     % list sequence folders inside this rat folder

% Accumulators for per-rat compilations
delta_waveform_broadband_comp = [];
delta_waveform_comp = [];

% Iterate over sequence/session folders (j indexes sequences)
j = 1;
while j <= length(g)
    % Reset per-sequence/session containers
    delta_waveform_broadband_total = {};
    delta_waveform_total = {};
    delta_waveform_broadband_total_visualization = {};
    
    cd(g{j})
    % checksequence returns ordered list of session subfolders for current sequence
    G = checksequence;
    
    %% Identify pre and post folders within this sequence
    % cfold  -> pre-sleep folders (names containing 'pre' / 'Pre'), excluding tests
    cfold3 = [];
    cfold = G(or(cellfun(@(x) ~isempty(strfind(x,'pre')), G), ...
                 cellfun(@(x) ~isempty(strfind(x,'Pre')), G)));
    for q = 1:length(cfold)
        if (~contains(cfold{q}, 'test') && ~contains(cfold{q}, 'Test'))
            cfold3 = [cfold3; cfold{q}];
        end
    end
    if ~isempty(cfold3)
        cfold = cellstr(cfold3)';
    end

    % cfold2 -> post-trial folders (names containing 'post' / 'Post'), excluding tests
    cfold3 = [];
    cfold2 = G(or(cellfun(@(x) ~isempty(strfind(x,'post')), G), ...
                  cellfun(@(x) ~isempty(strfind(x,'Post')), G)));
    for q = 1:length(cfold2)
        if (~contains(cfold2{q}, 'test') && ~contains(cfold2{q}, 'Test'))
            cfold3 = [cfold3; cfold2{q}];
        end
    end
    cfold2 = cellstr(cfold3)';
    
    % Remove any post folders that are not trial1..trial5 (ignore trial6 etc.)
    for ind = 1:length(cfold2)
      if ~(contains(cfold2{ind},'trial1') || contains(cfold2{ind},'trial2') || ...
           contains(cfold2{ind},'trial3') || contains(cfold2{ind},'trial4') || ...
           contains(cfold2{ind},'trial5') || contains(cfold2{ind},'Trial1') || ...
           contains(cfold2{ind},'Trial2') || contains(cfold2{ind},'Trial3') || ...
           contains(cfold2{ind},'Trial4') || contains(cfold2{ind},'Trial5'))
          cfold2{ind} = [];
      end
    end
    cfold2 = cfold2(~cellfun('isempty', cfold2));
    
    % Combine pre and post lists (order preserved)
    G = [cfold cfold2];
    
    % If no valid session folders, skip
    if isempty(G)
        no_folder = 1;
    else
        no_folder = 0;
        
        % Process each session subfolder inside the sequence
        for i = 1:length(G)
            clear states
            cd(G{i})
            
            % Find sleep scoring files in the session folder
            A = dir('*states*.mat');
            A = {A.name};
            % Guard: ensure we have one or more states files
            if sum(contains(A, 'states')) > 0
                % Filter for files that actually contain 'states' and not 'eeg'
                A = A(cellfun(@(x) ~isempty(strfind(x,'states')), A));
                A = A(~(cellfun(@(x) ~isempty(strfind(x,'eeg')), A)));
                
                if sum(contains(A, 'states')) > 0
                    % Load the states file(s). They should define variable 'states'
                    cellfun(@load, A);
                    
                    % Find PFC (prefrontal cortex) LFP file
                    Cortex = dir(strcat('*','PFC','*.mat'));
                    Cortex = Cortex.name;
                    Cortex = load(Cortex);
                    % Expecting variable named 'PFC' inside the .mat
                    Cortex = getfield(Cortex,'PFC');
                    % Scale factor applied in original pipeline
                    Cortex = Cortex .* (0.195);
                    
                    % Detect whether this session is a normal chunk or post-trial-5
                    if and(~contains(G{i},'trial5'), ~contains(G{i},'Trial5'))
                        % ----------------------------
                        % Normal session (single 45 min chunk)
                        % ----------------------------
                        
                        % Trim or pad states to 45*60 seconds (45 minutes)
                        if length(states) < 45*60
                            states = [states nan(1,45*60 - length(states))];
                        else
                            states = states(1:45*60);
                        end
                        
                        % Trim or pad cortex to 45*60*fn samples
                        if length(Cortex) < 45*60*fn
                            Cortex = [Cortex.' (nan(45*60*fn - length(Cortex),1).')];
                        else
                            Cortex = Cortex(1:45*60*fn).';
                        end
                        
                        % Replace NaNs with zeros (original behavior)
                        PFC = Cortex;
                        if sum(isnan(PFC)) ~= 0
                            PFC(isnan(PFC)) = 0;
                            states(isnan(states)) = 0;
                        end
                        
                        % (Unused) low-pass design left in script (kept for compatibility)
                        Wn1 = [320/(fn/2)]; % Cutoff approx 320 Hz
                        [b2,a2] = butter(3, Wn1);
                        
                        % Convert continuous PFC into 1-second epochs (columns)
                        e_t = 1;
                        e_samples = e_t * fn;   % samples per epoch (fn per second)
                        ch = length(PFC);
                        nc = floor(ch / e_samples); % number of full 1-s epochs
                        NC = [];
                        NC2 = [];
                        for kk = 1:nc
                          NC2(:,kk) = PFC(1 + e_samples*(kk-1) : e_samples*kk);
                        end
                        
                        % Build binary vector indicating selected sleep stage per second
                        vec_bin = states;
                        vec_bin(vec_bin ~= ss) = 0;
                        vec_bin(vec_bin == ss) = 1;
                        
                        % If no epochs of requested stage were found, skip (or handle "All" option)
                        if sum(vec_bin) == 0
                              delta_total_data{j,1}{i,1} = NaN;
                            if ss == 6
                                % If 'All', let vec_bin be all ones (previous code does vec_bin+1)
                                vec_bin = vec_bin + 1;
                            else
                                % No epochs for this stage; continue to next session
                                V_pfc = 0;
                                cd ..
                                continue
                            end
                        end
                        
                        % Find consecutive runs of selected-stage epochs and collect
                        % each continuous run as a single segment
                        v2 = ConsecutiveOnes(vec_bin);
                        v_index = find(v2 ~= 0);
                        v_values = v2(v2 ~= 0);
                        
                        % Build v_pfc: cell array where each entry is the concatenated
                        % broadband signal of a contiguous selected-stage period
                        for epoch_count = 1:length(v_index)
                            v_pfc{epoch_count,1} = reshape(NC2(:, v_index(epoch_count) : v_index(epoch_count) + (v_values(1,epoch_count)-1)), [], 1);
                        end 
                        
                        % Bandpass filter each contiguous segment to delta band (1-6 Hz)
                        Wn1=[1/(fn/2) 6/(fn/2)];
                        [b2,a2] = butter(3,Wn1);
                        V_pfc = cellfun(@(equis) filtfilt(b2,a2,equis), v_pfc, 'UniformOutput', false);
                        
                        % Concatenate bandpassed segments for detection
                        VV_pfc = [];
                        for b = 1:size(V_pfc,1)
                            VV_pfc = [VV_pfc; V_pfc{b}];
                        end
                        V_pfc = VV_pfc;
                        V_pfc = {V_pfc};  % wrap back into a cell for the following loop
                        
                        z = 0; % event counter for this session chunk
                        for p = 1:length(V_pfc)
                            V_pfc_bp = V_pfc{p}; % bandpassed concatenated signal
                            
                            % Build time vector at sampling rate fn
                            V_pfc_bp2 = [];
                            for l = 1:length(V_pfc_bp)
                                V_pfc_bp2(l,1) = l / fn;  % time in seconds
                            end
                            % detector expects [time, value] columns
                            V_pfc_bp = horzcat(V_pfc_bp2, V_pfc_bp);
                            
                            % Only run detection if we have enough data (>4 s here)
                            if length(V_pfc_bp2) > 4 * fn
                                delta = FindDeltaWaves(V_pfc_bp);
                                delta_total_data{j,1}{i,p} = delta;
                                z = z + size(delta,1);
                            else
                                delta_total_data{j,1}{i,p} = NaN;
                            end
                        end
                        
                        % Extract waveform snippets for each detected delta event
                        if iscell(v_pfc) && ~isempty(delta)
                            concatenated_NREM_broadband_pfc = vertcat(v_pfc{:});
                            waveforms_delta_broadband = {};
                            waveforms_delta_broadband_visualization = {};
                            for c = 1:size(delta,1)
                                % extract the exact start->end snippet (broadband)
                                waveforms_delta_broadband{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                
                                % build a larger window for visualization if possible (±10000 samples)
                                if (int32(delta(c,1)*fn + 1) > 10000) && ((int32(delta(c,3)*fn + 1) < (length(concatenated_NREM_broadband_pfc) - 10001)))
                                    waveforms_delta_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn - 10000) : int32(delta(c,3)*fn + 10000));
                                else
                                    waveforms_delta_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                end
                            end
                        else
                            waveforms_delta_broadband = NaN;
                            waveforms_delta_broadband_visualization = NaN;
                        end
                        
                        if iscell(V_pfc) && ~isempty(delta)
                            concatenated_NREM_pfc = vertcat(V_pfc{:});
                            waveforms_delta = {};
                            for c = 1:size(delta,1)
                                waveforms_delta{c,1} = concatenated_NREM_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                            end
                        else
                            waveforms_delta = NaN;
                        end
                        
                        % Store results for this session chunk
                        delta_waveform_broadband_total{i} = waveforms_delta_broadband;
                        delta_waveform_broadband_total_visualization{i} = waveforms_delta_broadband_visualization;
                        delta_waveform_total{i} = waveforms_delta;
                        total_delta(j,i) = z;
                        
                        % Compute events per minute normalization:
                        stage_count = sum(states(:) == ss);
                        total_delta_minute(j,i) = (total_delta(j,i) / stage_count * 60);
                        
                        % Clear temporary variables to free memory before next iteration
                        clear V_pfc v_pfc V_pfc_bp V_pfc_bp2 v_values vec_bin VV_pfc v2 v_index NC2 NC
                        
                    elseif contains(G{i}, 'rial5')
                        % ----------------------------
                        % PostTrial 5 case: split the long recording into 4x 45-min chunks
                        % (the code below is a repeated version of the above logic, adapted
                        %  to operate on PFC_1..PFC_4 and states1..states4)
                        %
                        % The block keeps the same workflow: pad/truncate, split into 4
                        % chunks, epoch each chunk, filter, detect, extract snippets,
                        % and save per-chunk results in indices i..i+3.
                        % ----------------------------
                        
                        % Ensure states and Cortex are 4 * 45 min long; pad/truncate
                        if length(states) < 45*60*4
                            states = [states nan(1,45*60*4 - length(states))];
                        else
                            states = states(1:45*60*4);
                        end
                        
                        if length(Cortex) < 45*60*fn*4
                            Cortex = [Cortex.' (nan(45*60*fn*4 - length(Cortex),1).')];
                        else
                            Cortex = Cortex(1:45*60*fn*4).';
                        end
                        
                        % Split into 4 chunks
                        states1 = states(1:2700);
                        states2 = states(2700+1 : 2700*2);
                        states3 = states(1 + 2700*2 : 2700*3);
                        states4 = states(1 + 2700*3 : 2700*4);
                        
                        PFC_1 = Cortex(1 : 2700*fn);
                        PFC_2 = Cortex(2700*fn + 1 : 2700*2*fn);
                        PFC_3 = Cortex(1 + 2700*2*fn : 2700*3*fn);
                        PFC_4 = Cortex(1 + 2700*3*fn : 2700*4*fn);
                        
                        % Replace NaNs inside each chunk with zeros (original behavior)
                        if sum(isnan(PFC_1)) ~= 0
                            PFC_1(isnan(PFC_1)) = 0;
                            states1(isnan(states1)) = 0;
                        end
                        if sum(isnan(PFC_2)) ~= 0
                            PFC_2(isnan(PFC_2)) = 0;
                            states2(isnan(states2)) = 0;
                        end
                        if sum(isnan(PFC_3)) ~= 0
                            PFC_3(isnan(PFC_3)) = 0;
                            states3(isnan(states3)) = 0;
                        end
                        if sum(isnan(PFC_4)) ~= 0
                            PFC_4(isnan(PFC_4)) = 0;
                            states4(isnan(states4)) = 0;
                        end
                        
                        % The following repeated blocks process PFC_1..PFC_4 in turn
                        % (The code below mirrors the normal session processing but for
                        %  each chunk, storing results at indices i, i+1, i+2, i+3.)
                        
                        % Chunk 1 processing
                        e_t = 1;
                        e_samples = e_t * fn;
                        ch = length(PFC_1);
                        nc = floor(ch / e_samples);
                        NC = [];
                        NC2 = [];
                        for kk = 1:nc
                          NC2(:,kk) = PFC_1(1 + e_samples*(kk-1) : e_samples*kk);
                        end
                        vec_bin = states1;
                        vec_bin(vec_bin ~= ss) = 0;
                        vec_bin(vec_bin == ss) = 1;
                        
                        if sum(vec_bin) ~= 0
                            v2 = ConsecutiveOnes(vec_bin);
                            v_index = find(v2 ~= 0);
                            v_values = v2(v2 ~= 0);
                            for epoch_count = 1:length(v_index)
                                v_pfc{epoch_count,1} = reshape(NC2(:, v_index(epoch_count) : v_index(epoch_count) + (v_values(1,epoch_count)-1)), [], 1);
                            end
                            
                            % Bandpass to delta (1-6 Hz)
                            Wn1=[1/(fn/2) 6/(fn/2)];
                            [b2,a2] = butter(3,Wn1);
                            V_pfc = cellfun(@(equis) filtfilt(b2,a2,equis), v_pfc ,'UniformOutput',false);
                            
                            VV_pfc = [];
                            for b = 1:size(V_pfc,1)
                                VV_pfc = [VV_pfc; V_pfc{b}];
                            end
                            V_pfc = VV_pfc;
                            V_pfc = {V_pfc};
                            
                            z = 0;
                            for p = 1:length(V_pfc)
                                V_pfc_bp = V_pfc{p};
                                V_pfc_bp2 = [];
                                for l = 1:length(V_pfc_bp)
                                    V_pfc_bp2(l,1) = l / fn;
                                end
                                V_pfc_bp = horzcat(V_pfc_bp2, V_pfc_bp);
                                if length(V_pfc_bp2) > 4 * fn
                                    delta = FindDeltaWaves(V_pfc_bp);
                                    delta_total_data{j,1}{i,p} = delta;
                                    z = z + size(delta,1);
                                else
                                    delta_total_data{j,1}{i,p} = NaN;
                                end
                            end
                            
                            if iscell(v_pfc) && ~isempty(delta)
                                concatenated_NREM_broadband_pfc = vertcat(v_pfc{:});
                                waveforms_delta_broadband = {};
                                waveforms_delta_broadband_visualization = {};
                                for c = 1:size(delta,1)
                                    waveforms_delta_broadband{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                    if (int32(delta(c,1)*fn + 1) > 10000) && ((int32(delta(c,3)*fn + 1) < (length(concatenated_NREM_broadband_pfc) - 10001)))
                                        waveforms_delta_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn - 10000) : int32(delta(c,3)*fn + 10000));
                                    else
                                        waveforms_delta_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                    end
                                end
                            else
                                waveforms_delta_broadband = NaN;
                                waveforms_delta_broadband_visualization = NaN;
                            end
                            
                            if iscell(V_pfc) && ~isempty(delta)
                                concatenated_NREM_pfc = vertcat(V_pfc{:});
                                waveforms_delta = {};
                                for c = 1:size(delta,1)
                                    waveforms_delta{c,1} = concatenated_NREM_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                end
                            else
                                waveforms_delta = NaN;
                            end
                            
                            delta_waveform_broadband_total{i} = waveforms_delta_broadband;
                            delta_waveform_broadband_total_visualization{i} = waveforms_delta_broadband_visualization;
                            delta_waveform_total{i} = waveforms_delta;
                            total_delta(j,i) = z;
                            stage_count = sum(states1(:) == ss);
                            total_delta_minute(j,i) = (total_delta(j,i) / stage_count * 60);
                        else
                            delta_total_data{j,1}{i,p} = NaN;
                            delta_waveform_broadband_total{i} = [];
                            delta_waveform_total{i} = [];
                            delta_waveform_broadband_total_visualization{i} = [];
                        end
                        
                        clear V_pfc v_pfc V_pfc_bp V_pfc_bp2 v_values vec_bin VV_pfc v2 v_index NC2 NC
                        
                        % Chunk 2 processing (same structure as chunk 1, results stored at i+1)
                        e_t = 1;
                        e_samples = e_t * fn;
                        ch = length(PFC_2);
                        nc = floor(ch / e_samples);
                        NC = [];
                        NC2 = [];
                        for kk = 1:nc
                          NC2(:,kk) = PFC_2(1 + e_samples*(kk-1) : e_samples*kk);
                        end
                        vec_bin = states2;
                        vec_bin(vec_bin ~= ss) = 0;
                        vec_bin(vec_bin == ss) = 1;
                        
                        if sum(vec_bin) ~= 0
                            v2 = ConsecutiveOnes(vec_bin);
                            v_index = find(v2 ~= 0);
                            v_values = v2(v2 ~= 0);
                            for epoch_count = 1:length(v_index)
                                v_pfc{epoch_count,1} = reshape(NC2(:, v_index(epoch_count) : v_index(epoch_count) + (v_values(1,epoch_count)-1)), [], 1);
                            end
                            
                            Wn1=[1/(fn/2) 6/(fn/2)];
                            [b2,a2] = butter(3,Wn1);
                            V_pfc = cellfun(@(equis) filtfilt(b2,a2,equis), v_pfc ,'UniformOutput',false);
                            
                            VV_pfc = [];
                            for b = 1:size(V_pfc,1)
                                VV_pfc = [VV_pfc; V_pfc{b}];
                            end
                            V_pfc = VV_pfc;
                            V_pfc = {V_pfc};
                            z = 0;
                            for p = 1:length(V_pfc)
                                V_pfc_bp = V_pfc{p};
                                V_pfc_bp2 = [];
                                for l = 1:length(V_pfc_bp)
                                    V_pfc_bp2(l,1) = l / fn;
                                end
                                V_pfc_bp = horzcat(V_pfc_bp2, V_pfc_bp);
                                if length(V_pfc_bp2) > 4 * fn
                                    delta = FindDeltaWaves(V_pfc_bp);
                                    delta_total_data{j,1}{i+1,p} = delta;
                                    z = z + size(delta,1);
                                else
                                    delta_total_data{j,1}{i+1,p} = NaN;
                                end
                            end
                            
                            if iscell(v_pfc) && ~isempty(delta)
                                concatenated_NREM_broadband_pfc = vertcat(v_pfc{:});
                                waveforms_delta_broadband = {};
                                waveforms_delta_broadband_visualization = {};
                                for c = 1:size(delta,1)
                                    waveforms_delta_broadband{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                    if (int32(delta(c,1)*fn + 1) > 10000) && ((int32(delta(c,3)*fn + 1) < (length(concatenated_NREM_broadband_pfc) - 10001)))
                                        waveforms_delta_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn - 10000) : int32(delta(c,3)*fn + 10000));
                                    else
                                        waveforms_delta_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                    end
                                end
                            else
                                waveforms_delta_broadband = NaN;
                                waveforms_delta_broadband_visualization = NaN;
                            end
                            
                            if iscell(V_pfc) && ~isempty(delta)
                                concatenated_NREM_pfc = vertcat(V_pfc{:});
                                waveforms_delta = {};
                                for c = 1:size(delta,1)
                                    waveforms_delta{c,1} = concatenated_NREM_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                end
                            else
                                waveforms_delta = NaN;
                            end
                            
                            delta_waveform_broadband_total{i+1} = waveforms_delta_broadband;
                            delta_waveform_broadband_total_visualization{i+1} = waveforms_delta_broadband_visualization;
                            delta_waveform_total{i+1} = waveforms_delta;
                            total_delta(j,i+1) = z;
                            stage_count = sum(states2(:) == ss);
                            total_delta_minute(j,i+1) = (total_delta(j,i+1) / stage_count * 60);
                        else
                            delta_total_data{j,1}{i+1,p} = NaN;
                            delta_waveform_broadband_total{i+1} = [];
                            delta_waveform_total{i+1} = [];
                            delta_waveform_broadband_total_visualization{i+1} = [];
                        end
                        
                        clear V_pfc v_pfc V_pfc_bp V_pfc_bp2 v_values vec_bin VV_pfc v2 v_index NC2 NC
                        
                        % Chunk 3 processing (i+2)
                        e_t = 1;
                        e_samples = e_t * fn;
                        ch = length(PFC_3);
                        nc = floor(ch / e_samples);
                        NC = [];
                        NC2 = [];
                        for kk = 1:nc
                          NC2(:,kk) = PFC_3(1 + e_samples*(kk-1) : e_samples*kk);
                        end
                        vec_bin = states3;
                        vec_bin(vec_bin ~= ss) = 0;
                        vec_bin(vec_bin == ss) = 1;
                        
                        if sum(vec_bin) ~= 0
                            v2 = ConsecutiveOnes(vec_bin);
                            v_index = find(v2 ~= 0);
                            v_values = v2(v2 ~= 0);
                            for epoch_count = 1:length(v_index)
                                v_pfc{epoch_count,1} = reshape(NC2(:, v_index(epoch_count) : v_index(epoch_count) + (v_values(1,epoch_count)-1)), [], 1);
                            end
                            
                            Wn1=[1/(fn/2) 6/(fn/2)];
                            [b2,a2] = butter(3,Wn1);
                            V_pfc = cellfun(@(equis) filtfilt(b2,a2,equis), v_pfc ,'UniformOutput',false);
                            
                            VV_pfc = [];
                            for b = 1:size(V_pfc,1)
                                VV_pfc = [VV_pfc; V_pfc{b}];
                            end
                            V_pfc = VV_pfc;
                            V_pfc = {V_pfc};
                            z = 0;
                            for p = 1:length(V_pfc)
                                V_pfc_bp = V_pfc{p};
                                V_pfc_bp2 = [];
                                for l = 1:length(V_pfc_bp)
                                    V_pfc_bp2(l,1) = l / fn;
                                end
                                V_pfc_bp = horzcat(V_pfc_bp2, V_pfc_bp);
                                if length(V_pfc_bp2) > 4 * fn
                                    delta = FindDeltaWaves(V_pfc_bp);
                                    delta_total_data{j,1}{i+2,p} = delta;
                                    z = z + size(delta,1);
                                else
                                    delta_total_data{j,1}{i+2,p} = NaN;
                                end
                            end
                            
                            if iscell(v_pfc) && ~isempty(delta)
                                concatenated_NREM_broadband_pfc = vertcat(v_pfc{:});
                                waveforms_delta_broadband = {};
                                waveforms_delta_broadband_visualization = {};
                                for c = 1:size(delta,1)
                                    waveforms_delta_broadband{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                    if (int32(delta(c,1)*fn + 1) > 10000) && ((int32(delta(c,3)*fn + 1) < (length(concatenated_NREM_broadband_pfc) - 10001)))
                                        waveforms_delta_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn - 10000) : int32(delta(c,3)*fn + 10000));
                                    else
                                        waveforms_delta_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                    end
                                end
                            else
                                waveforms_delta_broadband = NaN;
                                waveforms_delta_broadband_visualization = NaN;
                            end
                            
                            if iscell(V_pfc) && ~isempty(delta)
                                concatenated_NREM_pfc = vertcat(V_pfc{:});
                                waveforms_delta = {};
                                for c = 1:size(delta,1)
                                    waveforms_delta{c,1} = concatenated_NREM_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                end
                            else
                                waveforms_delta = NaN;
                            end
                            
                            delta_waveform_broadband_total{i+2} = waveforms_delta_broadband;
                            delta_waveform_broadband_total_visualization{i+2} = waveforms_delta_broadband_visualization;
                            delta_waveform_total{i+2} = waveforms_delta;
                            total_delta(j,i+2) = z;
                            stage_count = sum(states3(:) == ss);
                            total_delta_minute(j,i+2) = (total_delta(j,i+2) / stage_count * 60);
                        else
                            delta_total_data{j,1}{i+2,p} = NaN;
                            delta_waveform_broadband_total{i+2} = [];
                            delta_waveform_total{i+2} = [];
                            delta_waveform_broadband_total_visualization{i+2} = [];
                        end
                        
                        clear V_pfc v_pfc V_pfc_bp V_pfc_bp2 v_values vec_bin VV_pfc v2 v_index NC2 NC
                        
                        % Chunk 4 processing (i+3)
                        e_t = 1;
                        e_samples = e_t * fn;
                        ch = length(PFC_4);
                        nc = floor(ch / e_samples);
                        NC = [];
                        NC2 = [];
                        for kk = 1:nc
                          NC2(:,kk) = PFC_4(1 + e_samples*(kk-1) : e_samples*kk);
                        end
                        vec_bin = states4;
                        vec_bin(vec_bin ~= ss) = 0;
                        vec_bin(vec_bin == ss) = 1;
                        
                        if sum(vec_bin) ~= 0
                            v2 = ConsecutiveOnes(vec_bin);
                            v_index = find(v2 ~= 0);
                            v_values = v2(v2 ~= 0);
                            for epoch_count = 1:length(v_index)
                                v_pfc{epoch_count,1} = reshape(NC2(:, v_index(epoch_count) : v_index(epoch_count) + (v_values(1,epoch_count)-1)), [], 1);
                            end
                            
                            Wn1=[1/(fn/2) 6/(fn/2)];
                            [b2,a2] = butter(3,Wn1);
                            V_pfc = cellfun(@(equis) filtfilt(b2,a2,equis), v_pfc ,'UniformOutput',false);
                            
                            VV_pfc = [];
                            for b = 1:size(V_pfc,1)
                                VV_pfc = [VV_pfc; V_pfc{b}];
                            end
                            V_pfc = VV_pfc;
                            V_pfc = {V_pfc};
                            z = 0;
                            for p = 1:length(V_pfc)
                                V_pfc_bp = V_pfc{p};
                                V_pfc_bp2 = [];
                                for l = 1:length(V_pfc_bp)
                                    V_pfc_bp2(l,1) = l / fn;
                                end
                                V_pfc_bp = horzcat(V_pfc_bp2, V_pfc_bp);
                                if length(V_pfc_bp2) > 4 * fn
                                    delta = FindDeltaWaves(V_pfc_bp);
                                    delta_total_data{j,1}{i+3,p} = delta;
                                    z = z + size(delta,1);
                                else
                                    delta_total_data{j,1}{i+3,p} = NaN;
                                end
                            end
                            
                            if iscell(v_pfc) && ~isempty(delta)
                                concatenated_NREM_broadband_pfc = vertcat(v_pfc{:});
                                waveforms_delta_broadband = {};
                                waveforms_delta_broadband_visualization = {};
                                for c = 1:size(delta,1)
                                    waveforms_delta_broadband{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                    if (int32(delta(c,1)*fn + 1) > 10000) && ((int32(delta(c,3)*fn + 1) < (length(concatenated_NREM_broadband_pfc) - 10001)))
                                        waveforms_delta_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn - 10000) : int32(delta(c,3)*fn + 10000));
                                    else
                                        waveforms_delta_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                    end
                                end
                            else
                                waveforms_delta_broadband = NaN;
                                waveforms_delta_broadband_visualization = NaN;
                            end
                            
                            if iscell(V_pfc) && ~isempty(delta)
                                concatenated_NREM_pfc = vertcat(V_pfc{:});
                                waveforms_delta = {};
                                for c = 1:size(delta,1)
                                    waveforms_delta{c,1} = concatenated_NREM_pfc(int32(delta(c,1)*fn + 1) : int32(delta(c,3)*fn + 1));
                                end
                            else
                                waveforms_delta = NaN;
                            end
                            
                            delta_waveform_broadband_total{i+3} = waveforms_delta_broadband;
                            delta_waveform_broadband_total_visualization{i+3} = waveforms_delta_broadband_visualization;
                            delta_waveform_total{i+3} = waveforms_delta;
                            total_delta(j,i+3) = z;
                            stage_count = sum(states4(:) == ss);
                            total_delta_minute(j,i+3) = (total_delta(j,i+3) / stage_count * 60);
                        else
                            delta_total_data{j,1}{i+3,p} = NaN;
                            delta_waveform_broadband_total{i+3} = [];
                            delta_waveform_total{i+3} = [];
                            delta_waveform_broadband_total_visualization{i+3} = [];
                        end
                        
                        clear V_pfc v_pfc V_pfc_bp V_pfc_bp2 v_values vec_bin VV_pfc v2 v_index NC2 NC
                    end
                else
                    % No valid states file found inside this folder: go up one level
                    cd ..
                    continue
                end
            else
                % No states files at all
                cd ..
                continue
            end
            cd ..
        end
    end
    cd ..
    
    % Save per-session outputs for sequence g{j}
    save(strcat('delta_waveform_broadband_visualization_', g{j}, '.mat'), 'delta_waveform_broadband_total_visualization', '-v7.3')
    save(strcat('delta_waveform_broadband_', g{j}, '.mat'), 'delta_waveform_broadband_total', '-v7.3')
    save(strcat('delta_waveform_', g{j}, '.mat'), 'delta_waveform_total', '-v7.3')
    
    % Save timestamps and counts
    delta_timestamps_SD = delta_total_data{j}.';
    d_count = cellfun(@size, delta_timestamps_SD, 'UniformOutput', false);
    for d = 1:length(d_count)
        delta_count(d) = d_count{d}(1);
        if isnan(delta_timestamps_SD{d})
            delta_count(d) = 0;
        end 
    end
    save(strcat('delta_timestamps_', g{j}, '.mat'), 'delta_timestamps_SD', '-v7.3')
    save(strcat('delta_count_', g{j}, '.mat'), 'delta_count', '-v7.3')
    
    % Append to per-rat compilations and save them
    delta_waveform_broadband_comp = [delta_waveform_broadband_comp; delta_waveform_broadband_total];
    delta_waveform_comp = [delta_waveform_comp; delta_waveform_total];
    save(strcat('delta_waveform_broadband_compilation_Rat', rat_folder{k}, '.mat'), 'delta_waveform_broadband_comp', '-v7.3')
    save(strcat('delta_waveform_compilation_Rat', rat_folder{k}, '.mat'), 'delta_waveform_comp', '-v7.3')
    
    % Next sequence folder
    j = j + 1;
end
cd ..
