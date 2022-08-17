clearvars; clc; close all;
addpath(genpath('/home/genzel/Documents/CorticoHippocampal'))
addpath(genpath('/home/genzel/Documents/UMAP_Basic_OS/huseyin'))
addpath('/home/genzel/Documents/ADRITOOLS/')
cd('/media/genzel/genzel1/UMAP_NSD')
% cd('/media/genzel/genzel1/UMAP_Basic_OS')
% cd('/media/genzel/genzel1/RGS14_NSD/RGS_Rats')
ratnumber=input('Enter rat number: ')
rat_folder = getfolder;
rats=[];

for i=1:length(rat_folder)
    rats(i)=str2num(rat_folder{:,i})
end

ratindex=find(ratnumber==rats);
cd(rat_folder{ratindex})
daysnumber=getfolder;
ripple_waveform_broadband_compilation_variable=[];


for i=1:length(daysnumber)
    
    [Filename,path]=uigetfile('ripple_waveforms_broadband*.mat');
    File=fullfile(path,Filename)
    load(File);
    ripple_waveform_broadband_compilation_variable=[ripple_waveform_broadband_compilation_variable; ripple_waveform_broadband_total]

end
ripple_waveform_broadband_comp=ripple_waveform_broadband_compilation_variable;

save(strcat('ripple_waveforms_broadband_compilation_Rat',rat_folder{ratindex},'.mat'),'ripple_waveform_broadband_comp','-v7.3')
