% OS downsample
% This script downsamples electrophysiological (ephys) data for specified rats.
% It allows user interaction for selecting rats, acquisition frequencies, and conditions.
%You need the 'select_folder.m' function from Corticohippocampal: https://github.com/Aleman-Z/CorticoHippocampal/blob/master/Object%20space%20task/select_folder.m
addpath(genpath('/home/adrian/Documents/GitHub/CorticoHippocampal/Object space task'))

% Clear workspace and close figures
clear variables;
close all;

%You need the pre-designed files with information of Object Space tast from
%the UMAP github: https://github.com/genzellab/UMAP/tree/main/downsample
umap_github_path= '/home/adrian/Documents/GitHub/UMAP/downsample';

% Set paths for raw and downsampled data
folderpath_raw_data = '/kunefe/Rat_OS_Ephys_RGS14/Raw'; % Raw data directory for Rat 13
folderpath_downsampled_data = '/home/adrian/Documents/UMAP/rgs_downsampled';

% Change directory to downsampled data folder and load existing downsampled data
cd(umap_github_path);
load('OS_RGS14_UMAP_downsampling.mat');
cd(folderpath_downsampled_data)

% Define sampling frequencies for rats (in Hz)
fs_rats = ones(1, 9) * 30000; % CAREFUL, THESE VALUES are different for OS BASIC rats. Ask a core lab member. 

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

if ~isempty(stage)
    %Splits Multiple trials
    if ~isempty(stage(~isempty(strfind(an{1},','))))
        stage=stage(~isempty(strfind(an{1},',')));
        stage=stage{1};
        stage=strsplit(stage,',');
    end
end


%Adds trials containing an initial capital letter.
idx = isstrprop(stage,'upper') ;
if ~isempty(idx)
    for indexup=1:length(idx)
         varind=idx{indexup};
         if varind(1)~=1
             vj=stage{indexup};
             vj(1)=upper(vj(1));
             stage= [stage vj];
         end
    end
end

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
    
%Look for trial
if ~isempty(stage)
    Var=zeros(size(A));
    for j=1:length(stage)
    aver=cellfun(@(x) strfind(x,stage{j}),A,'UniformOutput',false);
    aver=cellfun(@(x) length(x),aver,'UniformOutput',false);
    Var=or(cell2mat(aver),Var);
    end
else
    Var=ones(size(A));    
end

%In case of extra folder
if Var==0 %Error: Var is a vector
    xo
 cd(A{1})
        A=getfolder;
        %Look for trial
        Var=zeros(size(A));
        for j=1:length(stage)
        aver=cellfun(@(x) strfind(x,stage{j}),A,'UniformOutput',false);
        aver=cellfun(@(x) length(x),aver,'UniformOutput',false);
        Var=or(cell2mat(aver),Var);
        end 
end
% xo
if ~isempty(stage)
    A=A(Var);
end

A=A.';

%% Label suggestion (Not used when All-trials option was selected)
str2=cell(size(A,1),1);

if ~isempty(stage)
    
   for j=1:length(stage)
       cont=0;
       for n=1:size(A,1)
              
            if n==1
                
            end
           
           %if contains(A{n},stage{j})
            if ~isempty(strfind(A{n},stage{j}))                
              cont=cont+1;  
              str2{n,1}=strcat(stage{j},num2str(cont));   

            end       
       end
     %str2{n,1}=strcat(stage{1},num2str(n));
   end
else
 str2=A;   
end   
   %%
%xo   
%LABEL TRIALS.

f = figure(2);
set(f, 'NumberTitle', 'off', ...
    'Name',strcat('Rat',num2str(Rat),'_',labelconditions{iii}));

c = uicontrol('Style','text','Position',[1 380 450 30]);
% c = uicontrol('Style','text','Position',[1 380 450 20]);
% c.String = {'Edit the Label column with the correct trial index according to the dates.'};
% c.String =sprintf('%s\n%s','Edit the Label column with the correct trial index according to the dates.','Leave blank if trial is corrupted.');
%{'Edit the Label column with the correct trial index according to the dates' 'Leave blank if trial is corrupted.'};
c.String =sprintf('%s\n%s','Select trials.','Leave blank label if trial is corrupted.');
c.FontSize=10;
c.FontAngle='italic';

uit = uitable(f);
% d = {A,str2};
uit.Data = [A str2];
uit.ColumnName={'File name'; 'Label'};
uit.ColumnWidth= {200,80};
% uit.Position = [20 20 258 78];


        
set(uit,'ColumnEditable',true(1,2))
h = uicontrol('Position',[350 20 100 40],'String','Confirm',...
              'Callback','uiresume(gcbf)');
h.FontSize=10;
uiwait(gcf); 
str2= get(uit,'Data');   
str2=str2(:,2);
%Remove corrupted trials.
close(f);
str1=A;
str1=str1(not(cellfun('isempty',str2)));
A=A(not(cellfun('isempty',str2)));
str2=str2(not(cellfun('isempty',str2)));
    
    
    
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
            HPC = load_open_ephys_data(cf1{ch});  % Load data for the first channel
            PFC = load_open_ephys_data(cf2{ch});  % Load data for the second channel
 
            % Downsample and filter the data
            HPC = filtfilt(b, a, HPC);  % Apply low-pass filter
            HPC = downsample(HPC, round(fs / fs_new));  % Downsample the data
            PFC = filtfilt(b, a, PFC);  % Apply low-pass filter
            PFC = downsample(PFC, round(fs / fs_new));  % Downsample the data
            %xo
            % Save downsampled data
         
            cd(dname2)
            %Rat folder
            if ~isfolder(num2str(Rat))
                mkdir(num2str(Rat))
            end
            cd(num2str(Rat))
            
    if ~isfolder(labelconditions2{iii})    
       mkdir(labelconditions2{iii})
    end
    cd(labelconditions2{iii})
            
    if ~exist(str2{num}, 'dir')
        mkdir(str2{num})
    end
cd(str2{num})
 save(['HPC_' cf1{1} '.mat'],'HPC')
 save(['PFC_' cf2{1} '.mat'],'PFC')
 clear PFC HPC 
 
 
cd(strcat(dname,'/',BB))    

 

    
        end

        % Update progress bar
        waitbar(num / length(str1), F);
    end

    % Close progress bar
    close(F);
    
    % Move to the next condition
    iii = iii + 1;
end
