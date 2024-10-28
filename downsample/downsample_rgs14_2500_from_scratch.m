% OS gui_downsample
% This script downsamples electrophysiological (ephys) data for specified rats.
% It allows user interaction for selecting rats, acquisition frequencies, and conditions.

% Clear workspace and close figures
clear variables;
close all;

% Set paths for raw and downsampled data
folderpath_raw_data = '/kunefe/Rat_OS_Ephys_RGS14/Raw'; % Raw data directory for Rat 13
folderpath_downsampled_data = '/home/adrian/Documents/UMAP/rgs_downsampled';

% Change directory to downsampled data folder and load existing downsampled data
cd(folderpath_downsampled_data);
load('OS_RGS14_UMAP_downsampling.mat');

% Define sampling frequencies for rats (in Hz)
fs_rats = ones(1, 9) * 30000;

% Select rat(s) via input dialog
opts.Resize = 'on';
opts.WindowStyle = 'modal';
opts.Interpreter = 'tex';
prompt = strcat('\bf Select a rat#. Options:','{ }', num2str(rats));
answer = inputdlg(prompt, 'Input', [2 30], {''}, opts);
Rat = str2double(answer{1});

% Input acquisition and new downsampled frequency
prompt = {'Enter acquisition frequency (Hz):', 'Enter new downsampled frequency (Hz):'};
dlgtitle = 'Input';
dims = [1 35];
definput = {num2str(fs_rats(find(rats == Rat))), '2500'};
answer = inputdlg(prompt, dlgtitle, dims, definput);
fs = str2num(answer{1});       % Original frequency
fs_new = str2num(answer{2});   % Downsampled frequency

% Initialize variables for trial selection
an = [];  
stage = an;  % Define stage variable for trial conditions

% Get ephys data folder for the selected rat
dname = uigetdir(folderpath_raw_data, strcat('Select folder with Ephys data for Rat', num2str(Rat)));
dname2 = uigetdir(folderpath_downsampled_data, 'Select folder where downsampled data should be saved');

% Select conditions for downsampling (checkbox GUI)
f = figure();  
movegui(gcf, 'center');

% Create checkboxes for selecting conditions
Boxcheck = cell(1, length(labelconditions));
for h1 = 1:length(labelconditions)
    boxcheck = uicontrol(f, 'Style', 'checkbox', 'String', labelconditions{h1}, 'Position', [10 f.Position(4) - 30 * h1 200 20]);
    boxcheck.FontSize = 11;
    boxcheck.Value = 1;
    Boxcheck{h1} = boxcheck;   
end

% Set up figure properties
set(f, 'NumberTitle', 'off', 'Name', 'Select conditions');

% Add continue button
c = uicontrol;
c.String = 'Continue';
c.FontSize = 10;
c.Position = [f.Position(1) / 3.5 c.Position(2) - 10 f.Position(3) / 2 c.Position(4)];

% Callback for the continue button
c.Callback = 'uiresume(gcbf)';
uiwait(gcf);  % Wait for user input

% Retrieve selected conditions
boxch = cellfun(@(x) get(x, 'Value'), Boxcheck);
clear Boxcheck;
labelconditions = labelconditions(find(boxch ~= 0));
labelconditions2 = labelconditions2(find(boxch ~= 0));
close(f);

% Iterate through selected conditions
iii = 1;
while iii <= length(labelconditions)
    cd(dname);  % Go to the ephys folder for the specified rat

    % Select folder for the current condition
    [BB, labelconditions, labelconditions2] = select_folder(Rat, iii, labelconditions, labelconditions2);
    cd(BB);
    A = getfolder;  % Get list of files in the selected folder
    
    % Trial selection based on user input
    if ~isempty(stage)
        Var = zeros(size(A));
        for j = 1:length(stage)
            aver = cellfun(@(x) strfind(x, stage{j}), A, 'UniformOutput', false);
            aver = cellfun(@(x) length(x), aver, 'UniformOutput', false);
            Var = or(cell2mat(aver), Var);
        end
    else
        Var = ones(size(A));  % Use all trials if no stage specified
    end

    % Check for additional folders if necessary
    if Var == 0
        cd(A{1});
        A = getfolder;  % Get files again from new directory
        Var = zeros(size(A));
        for j = 1:length(stage)
            aver = cellfun(@(x) strfind(x, stage{j}), A, 'UniformOutput', false);
            aver = cellfun(@(x) length(x), aver, 'UniformOutput', false);
            Var = or(cell2mat(aver), Var);
        end
    end

    if ~isempty(stage)
        A = A(Var);  % Filter files based on trials
    end
    
    % Prepare for labeling trials
    str2 = cell(size(A, 1), 1);
    if ~isempty(stage)
        for j = 1:length(stage)
            cont = 0;
            for n = 1:size(A, 1)
                if ~isempty(strfind(A{n}, stage{j}))
                    cont = cont + 1;  
                    str2{n, 1} = strcat(stage{j}, num2str(cont));  % Create label
                end       
            end
        end
    else
        str2 = A;  % Use file names as labels if no stage specified
    end   
    
    % Create GUI for labeling trials
    f = figure(2);
    set(f, 'NumberTitle', 'off', 'Name', strcat('Rat', num2str(Rat), '_', labelconditions{iii}));

    % Instruction text
    c = uicontrol('Style', 'text', 'Position', [1 380 450 30]);
    c.String = sprintf('%s\n%s', 'Select trials.', 'Leave blank label if trial is corrupted.');
    c.FontSize = 10;
    c.FontAngle = 'italic';

    % Create table for trial names and labels
    uit = uitable(f);
    uit.Data = [A str2];
    uit.ColumnName = {'File name'; 'Label'};
    uit.ColumnWidth = {200, 80};
    set(uit, 'ColumnEditable', true(1, 2));

    % Confirm button for labeling
    h = uicontrol('Position', [350 20 100 40], 'String', 'Confirm', 'Callback', 'uiresume(gcbf)');
    h.FontSize = 10;
    uiwait(gcf);  % Wait for confirmation

    % Get updated labels and remove corrupted trials
    str2 = get(uit, 'Data');   
    str2 = str2(:, 2);  % Extract label column
    str1 = A;
    str1 = str1(not(cellfun('isempty', str2)));  % Filter based on non-empty labels
    A = A(not(cellfun('isempty', str2)));  % Filter file names
    str2 = str2(not(cellfun('isempty', str2)));  % Filter labels

    % Initialize progress bar
    F = waitbar(0, 'Please wait...');
    
    % Loop through each trial for downsampling
    for num = 1:length(str1)
        chfol = getfolder;  % Get folder of channels
        if length(chfol) == 1
            cd(chfol{1});
        end

        cd(str1{num, 1});  % Change directory to the current trial

        % Filter setup for downsampling
        Wn = [fs_new / fs];  % Cutoff frequency
        [b, a] = butter(3, Wn);  % Low-pass filter coefficients

        % Load channels for the selected rat
        vr = getfield(channels, strcat('Rat', num2str(Rat)));  % Get electrode channels
        cfold = dir;  % List contents of the current directory
        cfold = {cfold.name};
        cfold = cfold(cellfun(@(x) ~isempty(strfind(x, 'CH')), cfold));  % Filter to channel files

        if isempty(cfold)
            dname3 = uigetdir([], strcat('Select folder where ephys data is stored'));
            cd(dname3);
        end

        % Select channels for HPC and PFC based on conditions
        if strcmp(label1{1}, 'HPC')
            cf1 = [cfold(cellfun(@(x) ~isempty(strfind(x, ['CH' num2str(vr(1)) '.'])), cfold)), cfold(cellfun(@(x) ~isempty(strfind(x, ['CH' num2str(vr(1)) '_'])), cfold))];
            cf2 = [cfold(cellfun(@(x) ~isempty(strfind(x, ['CH' num2str(vr(2)) '.'])), cfold)), cfold(cellfun(@(x) ~isempty(strfind(x, ['CH' num2str(vr(2)) '_'])), cfold))];
        else
            cf1 = [cfold(cellfun(@(x) ~isempty(strfind(x, ['CH' num2str(vr(1)) '.'])), cfold)), cfold(cellfun(@(x) ~isempty(strfind(x, ['CH' num2str(vr(1)) '_'])), cfold))];
            cf2 = [cfold(cellfun(@(x) ~isempty(strfind(x, ['CH' num2str(vr(2)) '.'])), cfold)), cfold(cellfun(@(x) ~isempty(strfind(x, ['CH' num2str(vr(2)) '_'])), cfold))];
        end

        % Process each selected channel
        for ch = 1:length(cf1)
            data1 = load(cf1{ch});  % Load data for the first channel
            data2 = load(cf2{ch});  % Load data for the second channel
            data1 = data1.data1;  % Extract the actual data
            data2 = data2.data2;  % Extract the actual data

            % Downsample and filter the data
            data1_filtered = filtfilt(b, a, data1);  % Apply low-pass filter
            data1_downsampled = downsample(data1_filtered, round(fs / fs_new));  % Downsample the data
            data2_filtered = filtfilt(b, a, data2);  % Apply low-pass filter
            data2_downsampled = downsample(data2_filtered, round(fs / fs_new));  % Downsample the data

            % Save downsampled data
            downsampled_name = fullfile(dname2, strcat('Rat', num2str(Rat), '_', labelconditions{iii}, '_', str1{num}, '_CH', num2str(ch), '.mat'));
            save(downsampled_name, 'data1_downsampled', 'data2_downsampled');  % Save both channels
        end

        % Update progress bar
        waitbar(num / length(str1), F);
    end

    % Close progress bar
    close(F);
    
    % Move to the next condition
    iii = iii + 1;
end
