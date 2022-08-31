%% SAME TRIAL, DIFFERENT CONDITION
clearvars
clc
close all
% x- Entropy; y- Mean Freq; z- Amplitude; l- AUC; q- Duration; p- Peak2Peak

% cd('/media/genzel/genzel1/UMAP_NSD/')
cd('/media/genzel/genzel1/UMAP_Basic_OS/13')
% cd('/media/genzel/genzel1/RGS14_NSD/RGS_Rats/6')


% prompt = {'Select a trial for comparison 1(presleep)-2(PT1)-3(PT2)-4(PT3)-5(PT4)-6(PT5.1)-7(PT5.2)-8(PT5.3)-9(PT5.4))'};
% dlgtitle = 'Choose between (1-9)';
% definput = {'9'};
% ChosenPT = inputdlg(prompt,dlgtitle,[1 80],definput); %Chosen PT for Characteristics
% m=str2double(ChosenPT{1, 1});

m=1; %1(presleep)-2(PT1)-3(PT2)-4(PT3)-5(PT4)-6(PT5.1)-7(PT5.2)-8(PT5.3)-9(PT5.4)

% OR 
[OR,path]=uigetfile('delta_waveform_broadband*.mat','Select OR');
File=fullfile(path,OR)
delta_waveform_broadband_total_OR=load(File);
deltas_OR_total=delta_waveform_broadband_total_OR.delta_waveform_broadband_total;

% HC
[HC,path]=uigetfile('delta_waveform_broadband*.mat','Select HC');
File=fullfile(path,HC)
delta_waveform_broadband_total_HC=load(File);
deltas_HC_total=delta_waveform_broadband_total_HC.delta_waveform_broadband_total;

% CN
[CN,path]=uigetfile('delta_waveform_broadband*.mat','Select CN');
File=fullfile(path,CN)
delta_waveform_broadband_total_CN=load(File);
deltas_CN_total=delta_waveform_broadband_total_CN.delta_waveform_broadband_total;

% OD
[OD,path]=uigetfile('delta_waveform_broadband*.mat','Select OD');
File=fullfile(path,OD)
delta_waveform_broadband_total_OD=load(File);
deltas_OD_total=delta_waveform_broadband_total_OD.delta_waveform_broadband_total;


% Trial by Trial  
deltas_HC = deltas_HC_total{1, m}';
deltas_OR = deltas_OR_total{1, m}';
deltas_OD = deltas_OD_total{1, m}';
deltas_CN = deltas_CN_total{1, m}';


si_index = cellfun(@(equis) sum(isnan(equis)), deltas_HC,'UniformOutput',false);
si_index= cell2mat(si_index);
si_index = ~logical(si_index);
deltas_HC= deltas_HC(si_index);

si_index = cellfun(@(equis) sum(isnan(equis)), deltas_OR,'UniformOutput',false);
si_index = cell2mat(si_index);
si_index = ~logical(si_index);
deltas_OR = deltas_OR(si_index); 

si_index = cellfun(@(equis) sum(isnan(equis)), deltas_OD,'UniformOutput',false);
si_index= cell2mat(si_index);
si_index = ~logical(si_index);
deltas_OD= deltas_OD(si_index);

si_index = cellfun(@(equis) sum(isnan(equis)), deltas_CN,'UniformOutput',false);
si_index = cell2mat(si_index);
si_index = ~logical(si_index);
deltas_CN = deltas_CN(si_index); 

Wn1=[100/(2500/2) 300/(2500/2)]; % Cutoff=100-300 Hz
[b1,a1] = butter(3,Wn1,'bandpass'); %Filter coefficients
deltas_OR = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_OR ,'UniformOutput',false);
deltas_HC = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_HC ,'UniformOutput',false);
deltas_OD = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_OD ,'UniformOutput',false);
deltas_CN = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_CN ,'UniformOutput',false);

% Entropy
x_or = cellfun(@(equis) entropy(equis),deltas_OR,'UniformOutput',false);
x_or = vertcat(x_or{:});
x_hc = cellfun(@(equis) entropy(equis),deltas_HC,'UniformOutput',false);
x_hc = vertcat(x_hc{:});
x_od = cellfun(@(equis) entropy(equis),deltas_OD,'UniformOutput',false);
x_od = vertcat(x_od{:});
x_cn = cellfun(@(equis) entropy(equis),deltas_CN,'UniformOutput',false);
x_cn = vertcat(x_cn{:});

% Mean Freqs
y_or = cellfun(@(equis) (meanfreq(equis,2500)),deltas_OR,'UniformOutput',false);
y_or = vertcat(y_or{:});
y_hc = cellfun(@(equis) (meanfreq(equis,2500)),deltas_HC,'UniformOutput',false);
y_hc = vertcat(y_hc{:});
y_od = cellfun(@(equis) (meanfreq(equis,2500)),deltas_OD,'UniformOutput',false);
y_od = vertcat(y_od{:});
y_cn = cellfun(@(equis) (meanfreq(equis,2500)),deltas_CN,'UniformOutput',false);
y_cn = vertcat(y_cn{:});

% Amplitude
z_or = cellfun(@(equis) max(abs(hilbert(equis))) ,deltas_OR,'UniformOutput',false);
z_or = vertcat(z_or{:});
z_hc = cellfun(@(equis) max(abs(hilbert(equis))),deltas_HC,'UniformOutput',false);
z_hc = vertcat(z_hc{:});
z_od = cellfun(@(equis) max(abs(hilbert(equis))) ,deltas_OD,'UniformOutput',false);
z_od = vertcat(z_od{:});
z_cn = cellfun(@(equis) max(abs(hilbert(equis))),deltas_CN,'UniformOutput',false);
z_cn = vertcat(z_cn{:});

% Area under curve
l_or = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_OR,'UniformOutput',false));
l_hc = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_HC,'UniformOutput',false));
l_od = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_OD,'UniformOutput',false));
l_cn = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_CN,'UniformOutput',false));

% Duration
q_or =(cellfun('length',deltas_OR)/2500);
q_hc = (cellfun('length',deltas_HC)/2500);
q_od =(cellfun('length',deltas_OD)/2500);
q_cn = (cellfun('length',deltas_CN)/2500);

% PeaktoPeak Amplitude
p_or = cellfun(@peak2peak,deltas_OR);
p_hc = cellfun(@peak2peak,deltas_HC);
p_od = cellfun(@peak2peak,deltas_OD);
p_cn = cellfun(@peak2peak,deltas_CN);

% Combination of characteristics 

l_hc = l_hc';
l_cn = l_cn';
l_od = l_od';
l_or = l_or';

q_hc = q_hc';
q_cn = q_cn';
q_od = q_od';
q_or = q_or';

p_hc = p_hc';
p_cn = p_cn';
p_od = p_od';
p_or = p_or';

totalCharacteristicsHC= [x_hc y_hc z_hc l_hc q_hc p_hc];
totalCharacteristicsCN= [x_cn y_cn z_cn l_cn q_cn p_cn];
totalCharacteristicsOD= [x_od y_od z_od l_od q_od p_od];
totalCharacteristicsOR= [x_or y_or z_or l_or q_or p_or];

% subplot(3,2,1)
% h1=histogram(x_or); title('Entropy');xlabel('Entropy');ylabel('Count')
% h1.FaceColor= [1 1 1]; h1.LineWidth=1;
% hold on
% h2=histogram(x_hc); title('Entropy');xlabel('Entropy');ylabel('Count')
% h2.FaceColor= [0.4940 0.1840 0.5560];
% h3=histogram(x_od); title('Entropy');xlabel('Entropy');ylabel('Count')
% h3.FaceColor= [0.7 0.7 0.7]; h3.LineWidth=0.4;
% hold on
% h4=histogram(x_cn); title('Entropy');xlabel('Entropy');ylabel('Count')
% h4.FaceColor= [0.8940 0.3840 0.6560];
% legend('OR', 'HC', 'OD', 'CN')
% alpha(0.7)
% hold off
% 
% subplot(3,2,2)
% 
% h1=histogram(y_or); title('Average Frequencies');xlabel('Frequency (Hz)');ylabel('Count')
% h1.BinWidth = 0.75;
% h1.FaceColor= [1 1 1];h1.LineWidth=1;
% hold on
% h2=histogram(y_hc); title('Average Frequencies');xlabel('Frequency (Hz)');ylabel('Count')
% h2.BinWidth = 0.75;
% h2.FaceColor= [0.4940 0.1840 0.5560];
% h3=histogram(y_od); title('Average Frequencies');xlabel('Frequency (Hz)');ylabel('Count')
% h3.BinWidth = 0.75;
% h3.FaceColor= [0.7 0.6 0.5];h3.LineWidth=0.4;
% hold on
% h4=histogram(y_cn); title('Average Frequencies');xlabel('Frequency (Hz)');ylabel('Count')
% h4.BinWidth = 0.75;
% h4.FaceColor= [0.2940 0.0840 0.2560];
% legend('OR', 'HC', 'OD', 'CN')
% alpha(0.7)
% xlim([120 220])
% hold off
% 
% 
% subplot(3,2,3)
% 
% h1=histogram(z_or); title('Amplitude');xlabel('\muV');ylabel('Count')
% h1.BinWidth = 2;
% h1.FaceColor= [1 1 1];h1.LineWidth=1;
% hold on
% h2=histogram(z_hc); title('Amplitude');xlabel('\muV');ylabel('Count')
% h2.BinWidth = 2;
% h2.FaceColor= [0.4940 0.1840 0.5560];
% legend('OR', 'HC')
% alpha(0.7)
%       xlim([0 100])
% hold off
% 
% 
% subplot(3,2,4)
% 
% h1=histogram(l_or); title('Area under the curve');xlabel('AUC');ylabel('Count')
% h1.BinWidth = 0.25;
% h1.FaceColor = [1 1 1]; h1.LineWidth=1;
% hold on
% h2=histogram(l_hc); title('Area under the curve');xlabel('AUC');ylabel('Count')
% h2.BinWidth = 0.25;
% h2.FaceColor = [0.4940 0.1840 0.5560];
% legend('OR', 'HC')
% alpha(0.7)
%         xlim([-1 10])
% hold off
% 
% subplot(3,2,5)
% 
% h1=histogram(q_or*2500); title('Duration');xlabel('Miliseconds');ylabel('Count') 
% h1.BinWidth = 2;
% h1.FaceColor = [1 1 1];h1.LineWidth=1;
% hold on
% h2=histogram(q_hc*2500); title('Duration');xlabel('Miliseconds');ylabel('Count')
% h2.BinWidth = 2;
% h2.FaceColor= [0.4940 0.1840 0.5560];
% legend('OR', 'HC')
% alpha(0.7)
%       xlim([30 200])
% hold off
% 
% subplot(3,2,6)
% 
% h1=histogram(p_or); title('Peak-to-peak amplitude');xlabel('\muV');ylabel('Count'); 
% h1.BinWidth = 8;
% h1.FaceColor = [1 1 1];h1.LineWidth=1;
% hold on
% h2=histogram(p_hc); title('Peak-to-peak amplitude');xlabel('\muV');ylabel('Count'); 
% h2.BinWidth = 8;
% h2.FaceColor= [0.4940 0.1840 0.5560];
% legend('OR', 'HC')
%  alpha(0.7)
% xlim([0 250])
% hold off
%             

