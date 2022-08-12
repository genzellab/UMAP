clearvars; clc;
addpath(genpath('/home/genzel/Documents/'))
addpath(genpath('/home/genzel/Documents/CorticoHippocampal'))
addpath(genpath('/home/genzel/Documents/UMAP_Basic_OS/huseyin'))
addpath(genpath('/media/genzel/genzel1/'))
addpath('/home/genzel/Documents/ADRITOOLS/')

[Split1,path1]=uigetfile('*.*','.mat','MultiSelect','on');
cd(path1)
fn=2500;
hpc1=Split1(find(contains(Split1,'HPC')))
File=fullfile(path1,hpc1{1,1})
hpc1=load(File);
f1=fieldnames(hpc1)
hpc1_=hpc1.HPC;
         
pfc1=Split1(find(contains(Split1,'PFC')))
File=fullfile(path1,pfc1{1,1})
pfc1=load(File);
f3=fieldnames(pfc1)
pfc1_=pfc1.PFC;



HPC1_timeonseconds=length(hpc1_)/2500
PFC1_timeonseconds=length(pfc1_)/2500

HPC1_timeonminutes=length(hpc1_)/2500/60
PFC1_timeonminutes=length(pfc1_)/2500/60


if length(hpc1_)~= length(pfc1_)   
    warning('Length mismatch')
    %Truncate
    if length(hpc1_)>length(pfc1_) 
        hpc1_=hpc1_(1:length(pfc1_));  
    else
        pfc1_=pfc1_(1:length(hpc1_));
    end
end

% 
% hpc2=load('HPC_100_CH46_2.continuous.mat') 
% f2=fieldnames(hpc2);
% pfc2=load('PFC_100_CH11_2.continuous.mat')
% f4=fieldnames(pfc2);

[Split2,path2]=uigetfile('*.*','.mat','MultiSelect','on');
cd(path2)
fn=2500;
hpc2=Split2(find(contains(Split2,'HPC')))
File=fullfile(path2,hpc2{1,1})
hpc2=load(File);
f2=fieldnames(hpc2)
hpc2_=hpc2.HPC;
         
pfc2=Split2(find(contains(Split2,'PFC')))
File=fullfile(path2,pfc2{1,1})
pfc2=load(File);
f4=fieldnames(pfc2)
pfc2_=pfc2.PFC;


if length(hpc2_)~= length(pfc2_)   
    warning('Length mismatch')
    if length(hpc2_)>length(pfc2_) 
        hpc2_=hpc2_(1:length(pfc2_));  
    else
        pfc2_=pfc2_(1:length(hpc2_));
    end
end

HPC2_timeonseconds=length(hpc2_)/2500
PFC2_timeonseconds=length(pfc2_)/2500

HPC2_timeonminutes=length(hpc2_)/2500/60
PFC2_timeonminutes=length(pfc2_)/2500/60

HPC=[hpc1.(f1{1});hpc2.(f2{1})];
save post_trial5_HPC_merged HPC;
PFC=[pfc1.(f3{1});pfc2.(f4{1})];
save post_trial5_PFC_merged PFC;

%% IF THERE IS 3 SPLIT 
% [Split3,path3]=uigetfile('*.*','.mat','MultiSelect','on');
% cd(path3)
% fn=2500;
% hpc3=Split3(find(contains(Split3,'HPC')))
% File=fullfile(path3,hpc3{1,1})
% hpc3=load(File);
% f5=fieldnames(hpc3)
% hpc3_=hpc3.HPC;
%          
% pfc3=Split3(find(contains(Split3,'PFC')))
% File=fullfile(path3,pfc3{1,1})
% pfc3=load(File);
% f6=fieldnames(pfc3)
% pfc3_=pfc3.PFC;
% 
% 
% if length(hpc3_)~= length(pfc3_)   
%     warning('Length mismatch')
% end
% 
% HPC3_timeonseconds=length(hpc3_)/2500
% PFC3_timeonseconds=length(pfc3_)/2500
% 
% HPC3_timeonminutes=length(hpc3_)/2500/60
% PFC3_timeonminutes=length(pfc3_)/2500/60
% 
% HPC=[hpc1.(f1{1});hpc2.(f2{1});hpc3.(f5{1})];
% save post_trial5_HPC_merged HPC;
% PFC=[pfc1.(f3{1});pfc2.(f4{1});pfc3.(f6{1})];
% save post_trial5_PFC_merged PFC;
