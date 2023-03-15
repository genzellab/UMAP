clear variables
clc
close all
addpath(genpath('/home/genzel/Documents/CorticoHippocampal'))
addpath('/home/genzel/Documents/ADRITOOLS/')
addpath('/media/genzel/genzel1')
cd('/media/genzel/genzel1/UMAP_Basic_OS') % Animal folders for Basic
% cd('/media/genzel/genzel1/UMAP_NSD') % Animal folders for NSD
% cd('/media/genzel/genzel1/RGS14_NSD/RGS_Rats') % Animal folders
rat_folder = getfolder;
% prompt = {'Enter the rat index'};
% dlgtitle = 'Rat Index';
% k = str2double(inputdlg(prompt,dlgtitle));
k = 7;
% for k = 1:length(rat_folder) % Iterates across animals
cd(rat_folder{k}) 
SD_folders  = getfolder; % List of SD folders

for j = 1:length(SD_folders); %Study day
waveforms = [];
timestamps = [];
%  for j = 1:length(SD_folders) % Iterates across SDs
waveforms =  struct2cell(load(strcat('ripple_waveforms_',SD_folders{j}, '.mat'))); % 1*9 cell array of waveforms
waveforms =  waveforms{1};
% waveforms =  struct2cell(load('ripple_waveforms_2018_06_27_Study_day_16_OR+NOV')); % 1*9 cell array of waveforms
% waveforms =  waveforms{1};
timestamps = struct2cell(load(strcat('ripple_total_data_',SD_folders{j}, '.mat'))); % 1*9 cell array of timestamps table
timestamps = timestamps{1};
% timestamps = struct2cell(load('ripple_total_data_2018_06_27_Study_day_16_OR+NOV')); % 1*9 cell array of timestamps table
% timestamps = timestamps{1};

count_short_ripple = [];
count_long_ripple = []; 
ripple_timestamps_short = [];
ripple_timestamps_long = [];  
    for i  = 1:length(waveforms) % Iterates across trials
        w = waveforms{i}; % waveforms and timestamps per trial
        t = timestamps{i};
        if ~isempty(w) & ~isempty(t)
            if ~isnan(t)
            duration = (cellfun('length',w)/2500); % duration per event in seconds; 2500 is the sampling rate
            duration = duration*1000; % Conversion into miliseconds
            short_ripple = find(duration<=100); %100ms is the threshold
            long_ripple = find(duration>100);
            count_short_ripple{i} = size(short_ripple,1); % counts per trial
            count_long_ripple{i} = size(long_ripple,1);
            ripple_timestamps_short{i} = t(short_ripple,:); % timestamps per trial 
            ripple_timestamps_long{i} = t(long_ripple,:);  
            clear duration
            else
            count_short_ripple{i} = 0;
            count_long_ripple{i} = 0; 
            ripple_timestamps_short{i} = NaN;
            ripple_timestamps_long{i} = NaN;       
            end
        else
        count_short_ripple{i} = 0;
        count_long_ripple{i} = 0; 
        ripple_timestamps_short{i} = NaN;
        ripple_timestamps_long{i} = NaN;    
        end
    end
    % Saving the counts and the timestamps
       save(strcat('Long_Short_Ripple_',SD_folders{j},'.mat'),'count_short_ripple','count_long_ripple','ripple_timestamps_short','ripple_timestamps_long')
%  end
'End of script'
clearvars -except SD_folders rat_folder k
% SD_folders.'
end
% cd .. 
% end
