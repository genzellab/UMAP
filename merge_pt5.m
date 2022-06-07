Rat=6;
cd('~/Documents/UMAP')
load('OS_RGS14_UMAP_downsampling.mat')

vr=getfield(channels,strcat('Rat',num2str(Rat)));%Electrode channels. 
%%

% cd('/media/irene/MD04_RAT_THETA/rat/Rat_OS_Ephys_RGS14/Rat_OS_Ephys_RGS14_rat6_373726/Rat_OS_Ephys_RGS14_rat6_373726_SD2_OR_06-07_02_2020')
cd('/media/irene/MD04_RAT_THETA/rat/Rat_OS_Ephys_RGS14/Rat_OS_Ephys_RGS14_rat6_373726/Rat_OS_Ephys_RGS14_rat6_373726_SD4_OD_15-16_02_2020')
%%
fs_new=1000;
fs=30000;

Wn=[fs_new/fs ]; % Cutoff=fs_new/2 Hz. 
[b,a] = butter(3,Wn);
% HPC=filtfilt(b,a,HPC);
% HPC=downsample(HPC,fs/fs_new);

HPC_1=load_open_ephys_data(['100_CH' num2str(vr(1)) '_0.continuous']);
HPC_1=filtfilt(b,a,HPC_1);
HPC_1=downsample(HPC_1,fs/fs_new);

PFC_1=load_open_ephys_data(['100_CH' num2str(vr(2)) '_0.continuous']);
PFC_1=filtfilt(b,a,PFC_1);
PFC_1=downsample(PFC_1,fs/fs_new);


 if length(HPC_1)>length(PFC_1)
                               HPC_1=HPC_1(1:length(PFC_1));
                           else
                               PFC_1=PFC_1(1:length(HPC_1));
 end
                           

%% %%

HPC_2=load_open_ephys_data(['100_CH' num2str(vr(1)) '_0.continuous']);
HPC_2=filtfilt(b,a,HPC_2);
HPC_2=downsample(HPC_2,fs/fs_new);

PFC_2=load_open_ephys_data(['100_CH' num2str(vr(2)) '_0.continuous']);
PFC_2=filtfilt(b,a,PFC_2);
PFC_2=downsample(PFC_2,fs/fs_new);


 if length(HPC_2)>length(PFC_2)
                               HPC_2=HPC_2(1:length(PFC_2));
                           else
                               PFC_2=PFC_2(1:length(HPC_2));
 end

%%
       HPC=[HPC_1; HPC_2];
       PFC=[PFC_1; PFC_2];
%%
 save(['HPC_100_' ['CH' num2str(vr(1)) '_0_SD4.continuous'] '.mat'],'HPC')
 save(['PFC_100_' ['CH' num2str(vr(2)) '_0_SD4.continuous'] '.mat'],'PFC')
