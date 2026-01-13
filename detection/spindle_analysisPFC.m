% spindle_analysisPFC.m
% -------------------------------------------------------------------------
% Detect spindles in PFC LFP across pre/post sessions and save timestamps,
% waveform snippets, phase information, counts, and per-rat compilations.
%
% High-level overview:
% - Walks rat -> sequence -> session folders (getfolder / checksequence).
% - Loads sleep scoring (*states*.mat) and PFC LFP (*PFC*.mat) files.
% - Selects epochs of the requested sleep stage (ss; default NREM = 3).
% - Converts continuous PFC into 1-second epochs and groups consecutive
%   epochs of the selected stage into contiguous segments.
% - Calls spindles_detection(...) which returns spindle timestamps and
%   related outputs for each contiguous segment; the detector receives
%   per-epoch timestamps and samples so it can return event times in seconds.
% - Extracts waveform snippets (broadband and filtered) for each detected
%   spindle, builds visualization windows when possible, and saves results.
%
% Outputs (per sequence/session and per rat):
% - spindles_waveforms_<session>.mat
% - spindles_waveforms_broadband_<session>.mat
% - spindles_waveforms_broadband_visualization_<session>.mat
% - spindles_count_<session>.mat
% - spindles_phase_<session>.mat
% - spindles_timestamps_<session>.mat
% - spindles_total_data_<session>.mat
% - spindles_data_compilation_Rat<rat>.mat (per-rat summary)
% - spindles_phases_compilation_Rat<rat>.mat
% - spindles_waveforms_compilation_Rat<rat>.mat
% - spindles_waveforms_broadband_compilation_Rat<rat>.mat
%
% Required helper functions / files:
% - getfolder    : return folder names in current directory
% - checksequence: return ordered session subfolders for a sequence
% - ConsecutiveOnes: helper used in other scripts (not directly called here)
% - spindles_detection(vec_bin, NC3, NC2, fn, j, i, k)
%     - Must accept: binary vector of target epochs (vec_bin),
%       NC3: per-epoch timestamps (seconds) matrix,
%       NC2: per-epoch samples matrix (broadband),
%       fn: sampling frequency (Hz),
%       j,i,k: indices (sequence, trial, rat) — passed through for logging.
%     - Returns: [spindles], phase_total, z (count), BST (bout timestamps),
%       V_pfc (filtered segments), v_pfc (broadband segments)
%
% Assumptions and notes:
% - Sampling rate fn is set near top (default 2500 Hz).
% - Session chunks are padded/truncated to 45 minutes (45*60 s).
% - Post-trial-5 sessions are treated as four consecutive 45-min chunks.
% - PFC variable in '*PFC*.mat' is scaled by factor 0.195 in this pipeline.
% - NaNs in signals and states are replaced with zeros (preserves original behavior).
% - The script currently uses a hardcoded rat index k=2 and processes a single
%   sequence (j loop limited). Change k and loop bounds to process all rats/sessions.
%
% Suggested improvements (not implemented here):
% - Parameterize top-level variables (fn, ss, pad length, scale factor).
% - Avoid replacing NaNs with zeros; skip NaN windows instead.
% - Factor repeated chunk processing into helper functions for clarity.
% - Add logging and error handling for missing variables/expected shapes.
% -------------------------------------------------------------------------

clear variables
clc
close all

% Add required toolbox/project paths (adjust to your system if needed)
addpath(genpath('/home/genzel/Documents/CorticoHippocampal'))
addpath(genpath('/home/genzel/Documents/UMAP_Basic_OS/huseyin'))
addpath('/home/genzel/Documents/ADRITOOLS/')
% Working directory - change to your dataset root as needed
% cd('/home/genzel/Documents/UMAP_Basic_OS/')
% cd('/media/genzel/genzel1/UMAP_Basic_OS/')
cd('/media/genzel/genzel1/UMAP_NSD/')
% cd('/media/genzel/genzel1/RGS14_NSD/RGS_Rats/')

% ---- TODO notes from original author ----
% - adapt NREM_min to counts!
% - raw and filtered in spindle (9-20) gui.
% - spindle gui will be used for delta (.5-4) either.
% - .5-20 for Cortex always!
% ------------------------------------------

% Sleep stage selection:
% Uncomment interactive block if you prefer GUI selection; currently fixed to NREM.
% list = {'Wake','NREM','Transitional','REM','All'};
% [indx1] = listdlg(...);
% switch indx1 ...
ss = 3;            % 3 == NREM by convention in these scripts
fn = 2500;         % sampling frequency (Hz)

% Initialize accumulators
total_spindles = [];
total_spindles_minute = [];
phase_total_complete = {};
rat_folder = getfolder;    % custom helper - returns list of rat folders

% NOTE: The script as written selects a single rat index (k = 2). To run for all
% rats, replace the following hardcoded selection by a loop:
% for k = 1:length(rat_folder)
k = 2;

% Enter rat folder and list sequence folders
cd(rat_folder{k})
g = getfolder;

% Per-rat compilation containers
spindle_phase_comp = [];
spindles_waveforms_comp = [];
spindles_waveforms_broadband_comp = [];

% The outer sequence loop is currently limited (j loop). Adjust as needed.
j = 1;
while j < 2
    % Process a single sequence g{j}; change to "for j=1:length(g)" to process all
    cd(g{j})
    % Get ordered session subfolders for this sequence
    G = checksequence;
    
    %% Find pre and post folders inside this sequence
    cfold3 = [];
    cfold = G(or(cellfun(@(x) ~isempty(strfind(x,'pre')),G), cellfun(@(x) ~isempty(strfind(x,'Pre')),G)));
    for q = 1:length(cfold)
        if (~contains(cfold{q}, 'test') && ~contains(cfold{q}, 'Test'))
            cfold3 = [cfold3; cfold{q}];
        end
    end
    if ~isempty(cfold3)
        cfold = cellstr(cfold3)';
    end

    cfold3 = [];
    cfold2 = G(or(cellfun(@(x) ~isempty(strfind(x,'post')),G), cellfun(@(x) ~isempty(strfind(x,'Post')),G)));
    for q = 1:length(cfold2)
        if (~contains(cfold2{q}, 'test') && ~contains(cfold2{q}, 'Test'))
            cfold3 = [cfold3; cfold2{q}];
        end
    end
    cfold2 = cellstr(cfold3)';

    % Ignore any post folders that are not trial1..trial5 (skip trial6 etc.)
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

    % Combine pre and post lists, process in that order
    G = [cfold cfold2];

    % If no valid session folders, skip this sequence
    if isempty(G)
        no_folder = 1;
    else
        no_folder = 0;

        % Iterate sessions/trials (i indexes trial or session folder)
        for i = 1:length(G)
            clear states
            cd(G{i})

            % Find sleep scoring files (*.mat containing 'states')
            A = dir('*states*.mat');
            A = {A.name};

            if sum(contains(A,'states')) > 0
                % Exclude files that contain 'eeg' in filename (if any)
                A = A(cellfun(@(x) ~isempty(strfind(x,'states')), A));
                A = A(~(cellfun(@(x) ~isempty(strfind(x,'eeg')), A)));

                if sum(contains(A,'states')) > 0
                    % Load states file(s) - they must create variable 'states'
                    cellfun(@load, A);

                    % Load PFC LFP file (expect variable PFC inside)
                    Cortex = dir(strcat('*','PFC','*.mat'));
                    Cortex = Cortex.name;
                    Cortex = load(Cortex);
                    Cortex = getfield(Cortex,'PFC');
                    % Apply pipeline-specific calibration / scale factor
                    Cortex = Cortex .* (0.195);

                    % ---------------------------------------------------------
                    % Branch handling:
                    % - Normal session: not trial5 -> single 45-min chunk
                    % - trial5 session: longer recording split into 4 chunks
                    % ---------------------------------------------------------
                    if and(~contains(G{i},'trial5'), ~contains(G{i},'Trial5'))
                        % ----------------------------
                        % Normal 45-minute session processing
                        % ----------------------------
                        % Ensure states vector is 45*60 seconds (pad/truncate)
                        if length(states) < 45*60
                            states = [states nan(1,45*60 - length(states))];
                        else
                            states = states(1:45*60);
                        end

                        % Ensure Cortex is 45*60*fn samples (pad/truncate)
                        if length(Cortex) < 45*60*fn
                            Cortex = [Cortex.' (nan(45*60*fn - length(Cortex),1).')];
                        else
                            Cortex = Cortex(1:45*60*fn).';
                        end

                        % Build continuous timestamps vector (seconds)
                        continuous_timestamps = [(0:length(Cortex)-1)/fn];

                        % Replace NaNs with zeros for both PFC and states (original behavior)
                        PFC = Cortex;
                        if sum(isnan(PFC)) ~= 0
                            PFC(isnan(PFC)) = 0;
                            states(isnan(states)) = 0;
                        end

                        % (Unused) LPF design kept for compatibility
                        Wn1 = [320/(fn/2)]; % Cutoff ~320 Hz
                        [b2,a2] = butter(3,Wn1);

                        % Convert continuous PFC and timestamps into 1-second epochs
                        e_t = 1;
                        e_samples = e_t * fn;  % samples per epoch (fn samples)
                        ch = length(PFC);
                        nc = floor(ch / e_samples); % number of full seconds
                        NC = [];
                        NC2 = [];
                        NC3 = [];
                        for kk = 1:nc
                            NC2(:,kk) = PFC(1 + e_samples*(kk-1) : e_samples*kk);
                            NC3(:,kk) = continuous_timestamps(1 + e_samples*(kk-1) : e_samples*kk);
                        end

                        % Build binary vector indicating selected sleep stage per second
                        vec_bin = states;
                        vec_bin(vec_bin ~= ss) = 0;
                        vec_bin(vec_bin == ss) = 1;

                        %% Event Detection - delegate to spindles_detection
                        % spindles_detection returns:
                        % spindles: matrix with event timestamps and info
                        % phase_total: phase information for events
                        % z: number of detected spindles
                        % BST: bout-specific timestamps
                        % V_pfc: filtered segments for extraction (cell)
                        % v_pfc: broadband segments for extraction (cell)
                        [spindles, phase_total, z, BST, V_pfc, v_pfc] = spindles_detection(vec_bin, NC3, NC2, fn, j, i, k);

                        % Extract waveform snippets (filtered) using event start/end columns
                        if iscell(V_pfc) && ~isempty(spindles)
                            concatenated_NREM_pfc = vertcat(V_pfc{:});
                            waveforms_spindles = {};
                            for c = 1:size(spindles,1)
                                % spindles(c,6) = start (s), spindles(c,8) = end (s)
                                waveforms_spindles{c,1} = concatenated_NREM_pfc(int32(spindles(c,6)*fn + 1) : int32(spindles(c,8)*fn + 1));
                            end
                        else
                            waveforms_spindles = NaN;
                        end

                        % Extract broadband snippets and larger visualization windows
                        if iscell(v_pfc) && ~isempty(spindles)
                            concatenated_NREM_broadband_pfc = vertcat(v_pfc{:});
                            waveforms_spindles_broadband = {};
                            waveforms_spindles_broadband_visualization = {};
                            for c = 1:size(spindles,1)
                                waveforms_spindles_broadband{c,1} = concatenated_NREM_broadband_pfc(int32(spindles(c,6)*fn + 1) : int32(spindles(c,8)*fn + 1));
                                % Build visualization window if enough samples exist (±7500 samples)
                                if (int32(spindles(c,6)*fn + 1) > 7500) && ((int32(spindles(c,8)*fn + 1) < (length(concatenated_NREM_broadband_pfc) - 7501)))
                                    waveforms_spindles_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(spindles(c,6)*fn - 7500) : int32(spindles(c,8)*fn + 7500));
                                else
                                    waveforms_spindles_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(spindles(c,6)*fn + 1) : int32(spindles(c,8)*fn + 1));
                                end
                            end
                        else
                            waveforms_spindles_broadband = NaN;
                            waveforms_spindles_broadband_visualization = NaN;
                        end

                        % Save results for this session/trial index i
                        spindles_waveform_broadband_total{i} = waveforms_spindles_broadband;
                        spindles_waveform_broadband_total_visualization{i} = waveforms_spindles_broadband_visualization;
                        spindles_waveform_total{i} = waveforms_spindles;
                        spindles_complete{j,i} = spindles;
                        spindles_bout_specific_timestamps{i} = BST;
                        phase_total_complete{j,1}{i,1} = phase_total;
                        total_spindles(j,i) = z;

                        % Normalize to events per minute using the number of stage seconds
                        stage_count = sum(states(:) == ss);
                        total_spindles_minute = (z / stage_count * 60);
                        total_spindles_minute_complete(j,i) = total_spindles_minute;

                        % Clear temporary variables to avoid leak/overlap
                        clear V_pfc v_pfc V_pfc_bp V_pfc_bp2 v_values vec_bin VV_pfc v2 v_index NC2 NC3 VV_timestamps VV_pfc_phase v_timestamps

                    elseif contains(G{i}, 'rial5')
                        % ----------------------------
                        % PostTrial 5 case: long recording split into 4 chunks of 45 min
                        % ----------------------------
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

                        % Process each of the four chunks
                        for jj = 1:4
                            % Extract chunk samples and corresponding states
                            PFC = Cortex((2700*fn*(jj-1))+1 : 2700*fn*jj);
                            states_chunk = states(2700*(jj-1)+1 : 2700*jj);

                            % Build timestamps for this chunk
                            continuous_timestamps = [(0:length(PFC)-1)/fn];

                            % Replace NaNs
                            if sum(isnan(PFC)) ~= 0
                                PFC(isnan(PFC)) = 0;
                                states_chunk(isnan(states_chunk)) = 0;
                            end

                            % Build 1-second epoch matrices for this chunk
                            e_t = 1;
                            e_samples = e_t * fn;
                            ch = length(PFC);
                            nc = floor(ch / e_samples);
                            NC2 = [];
                            NC3 = [];
                            for kk = 1:nc
                                NC2(:,kk) = PFC(1 + e_samples*(kk-1) : e_samples*kk);
                                NC3(:,kk) = continuous_timestamps(1 + e_samples*(kk-1) : e_samples*kk);
                            end

                            % Build binary vector for selected stage
                            vec_bin = states_chunk;
                            vec_bin(vec_bin ~= ss) = 0;
                            vec_bin(vec_bin == ss) = 1;

                            %% Event Detection for chunk (delegated)
                            [spindles, phase_total, z, BST, V_pfc, v_pfc] = spindles_detection(vec_bin, NC3, NC2, fn, j, i, k);

                            % Extract filtered snippets if available
                            if iscell(V_pfc) && ~isempty(spindles)
                                concatenated_NREM_pfc = vertcat(V_pfc{:});
                                waveforms_spindles = {};
                                for c = 1:size(spindles,1)
                                    waveforms_spindles{c,1} = concatenated_NREM_pfc(int32(spindles(c,6)*fn + 1) : int32(spindles(c,8)*fn + 1));
                                end
                            else
                                waveforms_spindles = NaN;
                            end

                            % Extract broadband snippets & visualization windows
                            if iscell(v_pfc) && ~isempty(spindles)
                                concatenated_NREM_broadband_pfc = vertcat(v_pfc{:});
                                waveforms_spindles_broadband = {};
                                waveforms_spindles_broadband_visualization = {};
                                for c = 1:size(spindles,1)
                                    waveforms_spindles_broadband{c,1} = concatenated_NREM_broadband_pfc(int32(spindles(c,6)*fn + 1) : int32(spindles(c,8)*fn + 1));
                                    if (int32(spindles(c,6)*fn + 1) > 7500) && ((int32(spindles(c,8)*fn + 1) < (length(concatenated_NREM_broadband_pfc) - 7501)))
                                        waveforms_spindles_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(spindles(c,6)*fn - 7500) : int32(spindles(c,8)*fn + 7500));
                                    else
                                        waveforms_spindles_broadband_visualization{c,1} = concatenated_NREM_broadband_pfc(int32(spindles(c,6)*fn + 1) : int32(spindles(c,8)*fn + 1));
                                    end
                                end
                            else
                                waveforms_spindles_broadband = NaN;
                                waveforms_spindles_broadband_visualization = NaN;
                            end

                            % Store chunk results at indices i+jj-1 to preserve overall session indexing
                            spindles_waveform_broadband_total{i+jj-1} = waveforms_spindles_broadband;
                            spindles_waveform_broadband_total_visualization{i+jj-1} = waveforms_spindles_broadband_visualization;
                            spindles_complete{j,i+jj-1} = spindles;
                            spindles_bout_specific_timestamps{i+jj-1} = BST;
                            phase_total_complete{j,1}{i+jj-1,1} = phase_total;
                            total_spindles(j,i+jj-1) = z;

                            stage_count = sum(states(:) == ss);
                            total_spindles_minute = (z / stage_count * 60);
                            total_spindles_minute_complete(j,i+jj-1) = total_spindles_minute;

                            clear V_pfc v_pfc V_pfc_bp V_pfc_bp2 v_values vec_bin VV_pfc v2 v_index NC2 NC3
                        end
                    else
                        % No relevant branch matched - continue to next folder
                        continue
                    end
                else
                    % No states file with expected name; go up and continue
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

    % After processing sequence g{j}, compile & save outputs
    phase_total = phase_total_complete{j}.';
    spindle_phase_comp = [spindle_phase_comp; phase_total];
    spindles_count = total_spindles(j,:);
    spindles_waveforms_comp = [spindles_waveforms_comp; spindles_waveform_total];
    spindles_waveforms_broadband_comp = [spindles_waveforms_broadband_comp; spindles_waveform_broadband_total];

    spindles_total_data = spindles_complete(j,:);

    % Write per-session files
    save(strcat('spindles_waveforms_', g{j}, '.mat'), 'spindles_waveform_total', '-v7.3')
    save(strcat('spindles_waveforms_broadband_', g{j}, '.mat'), 'spindles_waveform_broadband_total', '-v7.3')
    save(strcat('spindles_waveforms_broadband_visualization_', g{j}, '.mat'), 'spindles_waveform_broadband_total_visualization', '-v7.3')
    save(strcat('spindles_count_', g{j}, '.mat'), 'spindles_count')

    save(strcat('spindles_phase_', g{j}, '.mat'), 'phase_total')
    save(strcat('spindles_timestamps_', g{j}, '.mat'), 'spindles_bout_specific_timestamps')
    save(strcat('spindles_total_data_', g{j}, '.mat'), 'spindles_total_data')

    % Save per-rat compilations (when last sequence reached)
    if j == length(g)
        save(strcat('spindles_data_compilation_Rat', rat_folder{k}, '.mat'), 'total_spindles', 'total_spindles_minute', 'spindles_complete')
    end

    save(strcat('spindles_phases_compilation_Rat', rat_folder{k}, '.mat'), 'spindle_phase_comp')
    save(strcat('spindles_waveforms_compilation_Rat', rat_folder{k}, '.mat'), 'spindles_waveforms_comp', '-v7.3')
    save(strcat('spindles_waveforms_broadband_compilation_Rat', rat_folder{k}, '.mat'), 'spindles_waveforms_broadband_comp', '-v7.3')

    % Move to next sequence
    j = j + 1;
end
cd ..
