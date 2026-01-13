function [spindles,phase_total,z,BST,V_pfc,v_pfc,Sx,Ex,Mx] = spindles_detection(vec_bin,NC3,NC2,fn,j,i,k)
% spindles_detection
% -------------------------------------------------------------------------
% Detect spindle events within contiguous epochs of a selected sleep stage.
%
% Inputs
% - vec_bin : binary vector (1 x Nseconds) with 1 where the target sleep
%             stage is present and 0 otherwise (e.g., output of states==ss).
% - NC3     : matrix (samples_per_epoch x n_epochs) containing per-sample
%             timestamps (in seconds) for each 1-s epoch, organized so that
%             NC3(:,e) contains timestamps for epoch e.
% - NC2     : matrix (samples_per_epoch x n_epochs) containing the broadband
%             PFC samples for each 1-s epoch, organized similarly to NC3.
% - fn      : sampling frequency in Hz (e.g., 2500).
% - j,i,k   : indices passed through for bookkeeping (sequence, trial, rat).
%
% Outputs
% - spindles : MxC matrix with detected spindle events (timestamps, peak, etc.)
%              (returned by FindSpindlesRGS14). The script expects at least
%              columns containing start, peak, and end times in seconds.
% - phase_total : vector of spindle phases (phase of slow-oscillation at spindle peak)
% - z         : total number of detected spindles (scalar)
% - BST       : Bout-specific timestamps; cell array with start/peak/end per bout
% - V_pfc     : cell array of bandpassed (spindle band) concatenated segments
% - v_pfc     : cell array of broadband concatenated segments (for waveform extraction)
% - Sx, Ex, Mx: cell arrays; per-bout lists of spindle start times (Sx),
%               end times (Ex) and peak times (Mx)
%
% Behavior summary
% - Groups consecutive 1s epochs (vec_bin) into continuous bouts.
% - For each bout, concatenates the broadband signal and timestamps.
% - Filters broadband signal to spindle band (9-20 Hz) for detection.
% - Filters broadband signal to slow-oscillation band (0.5-4 Hz) to compute
%   instantaneous phase and assign a phase at the spindle peak.
% - Calls FindSpindlesRGS14 on the concatenated [time, signal] vector to
%   obtain spindle timestamps (function is external).
% - Maps global timestamps back to bout-specific windows and returns per-bout
%   structures.
%
% Requirements / assumptions
% - ConsecutiveOnes must return lengths of consecutive 1 runs (used to split bouts)
% - FindSpindlesRGS14(V_pfc_bp, k) must accept a Nx2 matrix [time(s), value]
%   and return a matrix of spindles with start/peak/end expressed in seconds
%   on the same time base.
% - NC2 and NC3 must align: NC3 contains timestamps for each sample in NC2.
% - Time units are seconds everywhere in this function.
% - The function is robust to no-detection cases (returns NaNs / empty values).
%
% Notes about outputs Sx/Ex/Mx and BST:
% - Sx, Ex, Mx are cell arrays of length equal to number of bouts. Each cell
%   contains a row vector of starts/ends/peaks (in global seconds) for spindles
%   that fell inside that bout.
% - BST is a Nx3 cell array [Sx, Ex, Mx] for convenience.
%
% -------------------------------------------------------------------------

% If there are any selected epochs (vec_bin contains ones), proceed.
if sum(vec_bin)~=0

    % Find consecutive runs of ones (bouts) and their lengths
    v2 = ConsecutiveOnes(vec_bin);
    v_index = find(v2~=0);            % start indices of bouts (in seconds)
    v_values = v2(v2~=0);            % lengths of each bout (in seconds)
    
    % For each contiguous bout, build two vectors:
    % - v_timestamps: per-sample timestamps (concatenated later)
    % - v_pfc       : per-sample broadband PFC signal (concatenated later)
    for epoch_count = 1:length(v_index)
        % Flatten the epoch-by-epoch matrices to produce continuous per-bout vectors
        v_timestamps{epoch_count,1} = reshape(NC3(:, v_index(epoch_count) : v_index(epoch_count) + (v_values(1,epoch_count)-1)), [], 1);
        v_pfc{epoch_count,1}       = reshape(NC2(:, v_index(epoch_count) : v_index(epoch_count) + (v_values(1,epoch_count)-1)), [], 1);
    end
    
    %% Filters design
    % Spindle band: 9-20 Hz
    Wn1 = [9/(fn/2) 20/(fn/2)]; 
    [b2,a2] = butter(3,Wn1); % 3rd-order Butterworth bandpass for spindles
    
    % Slow-oscillation band: 0.5-4 Hz (used to compute phase)
    Wn1 = [0.5/(fn/2) 4/(fn/2)];
    [b3,a3] = butter(3,Wn1); % 3rd-order Butterworth bandpass for SO
    
    % Apply filters to each bout (v_pfc is the broadband signal per bout)
    V_pfc = cellfun(@(equis) filtfilt(b2,a2,equis), v_pfc ,'UniformOutput',false); % spindle-band filtered (for detection)
    v_pfc_phase = cellfun(@(equis) filtfilt(b3,a3,equis), v_pfc ,'UniformOutput',false); % SO-filtered signal (for phase)
    % Instantaneous phase in degrees (0..360) for each sample of each bout
    V_pfc_phase = cellfun(@(equis) mod(rad2deg(angle(hilbert(equis))),360), v_pfc_phase, 'UniformOutput', false);

    %% Concatenate all bouts into continuous vectors for detection
    VV_pfc = [];
    VV_timestamps = [];
    VV_pfc_phase = [];
    for b = 1:size(V_pfc,1) % iterate bouts
        VV_pfc = [VV_pfc; V_pfc{b}];                % concatenated filtered signal
        VV_timestamps = [VV_timestamps; v_timestamps{b}]; % concatenated timestamps (original time base)
        VV_pfc_phase = [VV_pfc_phase; V_pfc_phase{b}];   % concatenated phase vector (aligned with VV_pfc)
    end

    z = 0; % total count of spindles for these bouts (will be updated)
    % Build a time vector in seconds for the concatenated samples on a presumed
    % continuous 1/fn grid. (This makes a second timescale referenced to "NREM")
    VV_timestamps_NREM = [0:length(VV_timestamps)-1].' ./ fn;

    % Detector expects [time (s), value] columns
    V_pfc_bp = horzcat(VV_timestamps, VV_pfc);
    V_pfc_bp_NREM = horzcat(VV_timestamps_NREM, VV_pfc); % not used directly here

    %% Spindles detection and phase extraction
    if length(VV_timestamps) > 10000 % require enough samples to run detector (≈4s @ 2500Hz -> adjust)
        % Call external detector which returns spindle timestamps in seconds
        spindles = FindSpindlesRGS14(V_pfc_bp, k);

        if ~isempty(spindles)
            % Map spindle timestamps (reported in global time) to the NREM-relative
            % concatenated time vector indices. The mapping strategy here:
            % - For each spindle time reported in spindles(:,1..3) (start, peak, end),
            %   find the matching indices in VV_timestamps via integer rounding at fn.
            % - Then readout the corresponding VV_timestamps_NREM entries, generating
            %   a version of spindles in the NREM-relative time base (spindles_NREM).
            spindles_NREM(:,1) = VV_timestamps_NREM(find(ismember(int32(VV_timestamps*fn), int32(spindles(:,1)*fn))));
            spindles_NREM(:,2) = VV_timestamps_NREM(find(ismember(int32(VV_timestamps*fn), int32(spindles(:,2)*fn))));
            spindles_NREM(:,3) = VV_timestamps_NREM(find(ismember(int32(VV_timestamps*fn), int32(spindles(:,3)*fn))));

            % Store raw per-sequence detection results in a higher-level container
            spindles_total_data{j,1}{i,1} = spindles;
            z = z + size(spindles,1); % increment count by number of detected events

            % Find the phase at spindle peak: find indices where peak timestamps match concatenated timestamps
            phase_index = find(ismember(int32(VV_timestamps*fn), int32(spindles(:,2)*fn)));
            phase_total = VV_pfc_phase(phase_index); % phases corresponding to each spindle peak

            %% Conversion to Bout-Specific Timestamps
            % We need to assign each spindle to the bout it belongs to and
            % compute per-bout start/peak/end arrays.
            duration_epoch_cumsum = cumsum(v_values); % cumulative durations (seconds) per bout

            for f = 1:epoch_count % iterate per bout
                % Find spindles that fall inside the f-th bout using global timestamps
                % The v_timestamps{f} array contains the first..last timestamp of bout f,
                % so spindles with start>=first and end<=last belong to this bout.
                vec = find(spindles(:,1) >= v_timestamps{f}(1,1) & spindles(:,3) <= v_timestamps{f}(end,1));

                spindle_per_epoch(f) = length(vec);

                % Mark which bout (f) each spindle belongs to at column 5
                spindles(vec,5) = f;

                % Assign each spindle local start/peak/end times relative to bout.
                % spindles_NREM has start/peak/end expressed in the concatenated NREM-relative times,
                % so we store those in columns 6:8 for local times.
                spindles(vec, 6:8) = spindles_NREM(vec, 1:3);

                % Collect start/peak/end lists per bout into Sx, Ex, Mx
                Sx(f,1) = {spindles(vec,1).'}; % start times (global)
                Ex(f,1) = {spindles(vec,3).'}; % end times (global)
                Mx(f,1) = {spindles(vec,2).'}; % peak times (global)

                % BST is the per-bout assembled start/peak/end structure
                BST = [Sx, Ex, Mx];
            end
        else
            % No spindles found: set placeholders
            phase_total{1,i} = [];
            BST = [];
        end
    end

    % Record total spindles count in a global variable (caller may expect this)
    total_spindles(j,i) = z;

else
    % No selected epochs (vec_bin all zeros) -> return NaN/zero outputs
    spindles = NaN;
    spindles_total_data{j,1}{i,1} = NaN;
    phase_total = NaN;
    spindles_uncontinuous_timestamps{j,1}{i,1} = NaN;
    total_spindles(j,i) = 0;
    z = 0;
    BST = NaN;
    Sx = NaN;
    Mx = NaN;
    Ex = NaN;
    V_pfc = 0;
    v_pfc = 0;
end
end
