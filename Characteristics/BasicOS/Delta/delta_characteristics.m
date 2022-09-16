%% SAME TRIAL, DIFFERENT CONDITION
clearvars
clc
close all
% x- Entropy; y- Mean Freq; z- Amplitude; l- AUC; q- Duration; p- Peak2Peak

%cd('/media/genzel/genzel1/UMAP_NSD/6_39')
cd('/media/genzel/genzel1/UMAP_Basic_OS/9')
%cd('/media/genzel/genzel1/RGS14_NSD/RGS_Rats/1')


% prompt = {'Select a trial for comparison 1(presleep)-2(PT1)-3(PT2)-4(PT3)-5(PT4)-6(PT5.1)-7(PT5.2)-8(PT5.3)-9(PT5.4))'};
% dlgtitle = 'Choose between (1-9)';
% definput = {'9'};
% ChosenPT = inputdlg(prompt,dlgtitle,[1 80],definput); %Chosen PT for Characteristics
% m=str2double(ChosenPT{1, 1});
% OR 
% [OR,path]=uigetfile('delta_waveform_broadband*.mat','Select OR');
% File=fullfile(path,OR)
% delta_waveform_broadband_total_OR=load(File);
% deltas_OR_total=delta_waveform_broadband_total_OR.delta_waveform_broadband_total;
% 
% % HC
% [HC,path]=uigetfile('delta_waveform_broadband*.mat','Select HC');
% File=fullfile(path,HC)
% delta_waveform_broadband_total_HC=load(File);
% deltas_HC_total=delta_waveform_broadband_total_HC.delta_waveform_broadband_total;
% 
% % CN
% [CN,path]=uigetfile('delta_waveform_broadband*.mat','Select CN');
% File=fullfile(path,CN)
% delta_waveform_broadband_total_CN=load(File);
% deltas_CN_total=delta_waveform_broadband_total_CN.delta_waveform_broadband_total;
% 
% % OD
% [OD,path]=uigetfile('delta_waveform_broadband*.mat','Select OD');
% File=fullfile(path,OD)
% delta_waveform_broadband_total_OD=load(File);
% deltas_OD_total=delta_waveform_broadband_total_OD.delta_waveform_broadband_total;

m=9; %1(presleep)-2(PT1)-3(PT2)-4(PT3)-5(PT4)-6(PT5.1)-7(PT5.2)-8(PT5.3)-9(PT5.4)

[Conditions,path]=uigetfile('delta_waveform_broadband*.mat','MultiSelect','on');

OR=Conditions(find(contains(Conditions,'OR')))
if ~isempty(OR)
FileOR=fullfile(path,OR{1,end})
delta_waveform_broadband_total_OR=load(FileOR);
deltas_OR_total=delta_waveform_broadband_total_OR.delta_waveform_broadband_total;
deltas_OR = deltas_OR_total{1, m}';
else
    deltas_OR = {};
end

HC=Conditions(find(contains(Conditions,'HC')))
if ~isempty(HC)
FileHC=fullfile(path,HC{1,1})
delta_waveform_broadband_total_HC=load(FileHC);
deltas_HC_total=delta_waveform_broadband_total_HC.delta_waveform_broadband_total;
deltas_HC = deltas_HC_total{1, m}';
else
    deltas_HC = {};
end 

CN=Conditions(find(contains(Conditions,'CN')))
if ~isempty(CN)
FileCN=fullfile(path,CN{1,1})
delta_waveform_broadband_total_CN=load(FileCN);
deltas_CN_total=delta_waveform_broadband_total_CN.delta_waveform_broadband_total;
deltas_CN = deltas_CN_total{1, m}';
else
    deltas_CN = {};
end 

OD=Conditions(find(contains(Conditions,'OD')))
if ~isempty(OD)
FileOD=fullfile(path,OD{1,1})
delta_waveform_broadband_total_OD=load(FileOD);
deltas_OD_total=delta_waveform_broadband_total_OD.delta_waveform_broadband_total;
deltas_OD = deltas_OD_total{1, m}';
else
    deltas_OD = {};
end 

OR_N=Conditions(find(contains(Conditions,'OR_N')))
if ~isempty(OR_N)
FileOR_N=fullfile(path,OR_N{1,end})
delta_waveform_broadband_total_OR_N=load(FileOR_N);
deltas_OR_N_total=delta_waveform_broadband_total_OR_N.delta_waveform_broadband_total;
deltas_OR_N = deltas_OR_N_total{1, m}';
else
    deltas_OR_N = {};
end 

OR_N_S=Conditions(find(contains(Conditions,'OR_N_S')))
if ~isempty(OR_N_S)
FileOR_N_S=fullfile(path,OR_N_S{1,1})
delta_waveform_broadband_total_OR_N_S=load(FileOR_N_S);
deltas_OR_N_S_total=delta_waveform_broadband_total_OR_N_S.delta_waveform_broadband_total;
deltas_OR_N_S = deltas_OR_N_S_total{1, m}';
else
    deltas_OR_N_S = {};
end 

OR_NN_S=Conditions(find(contains(Conditions,'OR_NN_S')))
if ~isempty(OR_NN_S)
FileOR_NN_S=fullfile(path,OR_NN_S{1,1})
delta_waveform_broadband_total_OR_NN_S=load(FileOR_NN_S);
deltas_OR_NN_S_total=delta_waveform_broadband_total_OR_NN_S.delta_waveform_broadband_total;
deltas_OR_NN_S = deltas_OR_NN_S_total{1, m}';
else
    deltas_OR_NN_S = {};
end 


if ~isempty(deltas_HC)
    si_index = cellfun(@(equis) sum(isnan(equis)), deltas_HC,'UniformOutput',false);
    si_index= cell2mat(si_index);
    si_index = ~logical(si_index);
    deltas_HC= deltas_HC(si_index);
end

if ~isempty(deltas_OR)
    si_index = cellfun(@(equis) sum(isnan(equis)), deltas_OR,'UniformOutput',false);
    si_index = cell2mat(si_index);
    si_index = ~logical(si_index);
    deltas_OR = deltas_OR(si_index); 
end


if ~isempty(deltas_OD)
    si_index = cellfun(@(equis) sum(isnan(equis)), deltas_OD,'UniformOutput',false);
    si_index= cell2mat(si_index);
    si_index = ~logical(si_index);
    deltas_OD= deltas_OD(si_index);
end


if ~isempty(deltas_CN)
    si_index = cellfun(@(equis) sum(isnan(equis)), deltas_CN,'UniformOutput',false);
    si_index = cell2mat(si_index);
    si_index = ~logical(si_index);
    deltas_CN = deltas_CN(si_index); 
end

if ~isempty(deltas_OR_N)
    si_index = cellfun(@(equis) sum(isnan(equis)), deltas_OR_N,'UniformOutput',false);
    si_index = cell2mat(si_index);
    si_index = ~logical(si_index);
    deltas_OR_N = deltas_OR_N(si_index); 
end

if ~isempty(deltas_OR_N_S)
    si_index = cellfun(@(equis) sum(isnan(equis)), deltas_OR_N_S,'UniformOutput',false);
    si_index = cell2mat(si_index);
    si_index = ~logical(si_index);
    deltas_OR_N_S = deltas_OR_N_S(si_index); 
end

if ~isempty(deltas_OR_NN_S)
    si_index = cellfun(@(equis) sum(isnan(equis)), deltas_OR_NN_S,'UniformOutput',false);
    si_index = cell2mat(si_index);
    si_index = ~logical(si_index);
    deltas_OR_NN_S = deltas_OR_NN_S(si_index); 
end


Wn1=[100/(2500/2) 300/(2500/2)]; % Cutoff=100-300 Hz
[b1,a1] = butter(3,Wn1,'bandpass'); %Filter coefficients

if ~isempty(deltas_OR)
deltas_OR = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_OR ,'UniformOutput',false);
end
if ~isempty(deltas_HC)
deltas_HC = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_HC ,'UniformOutput',false);
end
if ~isempty(deltas_OD)
deltas_OD = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_OD ,'UniformOutput',false);
end
if ~isempty(deltas_CN)
deltas_CN = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_CN ,'UniformOutput',false);
end
if ~isempty(deltas_OR_N)
deltas_OR_N = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_OR_N ,'UniformOutput',false);
end
if ~isempty(deltas_OR_N_S)
deltas_OR_N_S = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_OR_N_S ,'UniformOutput',false);
end
if ~isempty(deltas_OR_NN_S)
deltas_OR_NN_S = cellfun(@(equis)filtfilt(b1,a1,equis),deltas_OR_NN_S ,'UniformOutput',false);
end

if isempty(deltas_HC)
    deltas_HC={};
end
if isempty(deltas_OR)
    deltas_OR={};
end
if isempty(deltas_OD)
    deltas_OD={};
end
if isempty(deltas_CN)
    deltas_CN={};
end
if isempty(deltas_OR_N)
    deltas_OR_N={};
end
if isempty(deltas_OR_N_S)
    deltas_OR_N_S={};
end
if isempty(deltas_OR_NN_S)
    deltas_OR_NN_S={};
end


% Entropy
x_or = cellfun(@(equis) entropy(equis),deltas_OR,'UniformOutput',false);
x_or = vertcat(x_or{:});
x_hc = cellfun(@(equis) entropy(equis),deltas_HC,'UniformOutput',false);
x_hc = vertcat(x_hc{:});
x_od = cellfun(@(equis) entropy(equis),deltas_OD,'UniformOutput',false);
x_od = vertcat(x_od{:});
x_cn = cellfun(@(equis) entropy(equis),deltas_CN,'UniformOutput',false);
x_cn = vertcat(x_cn{:});
x_or_n = cellfun(@(equis) entropy(equis),deltas_OR_N,'UniformOutput',false);
x_or_n = vertcat(x_or_n{:});
x_or_n_s = cellfun(@(equis) entropy(equis),deltas_OR_N_S,'UniformOutput',false);
x_or_n_s = vertcat(x_or_n_s{:});
x_or_nn_s = cellfun(@(equis) entropy(equis),deltas_OR_NN_S,'UniformOutput',false);
x_or_nn_s = vertcat(x_or_nn_s{:});

% Mean Freqs
y_or = cellfun(@(equis) (meanfreq(equis,2500)),deltas_OR,'UniformOutput',false);
y_or = vertcat(y_or{:});
y_hc = cellfun(@(equis) (meanfreq(equis,2500)),deltas_HC,'UniformOutput',false);
y_hc = vertcat(y_hc{:});
y_od = cellfun(@(equis) (meanfreq(equis,2500)),deltas_OD,'UniformOutput',false);
y_od = vertcat(y_od{:});
y_cn = cellfun(@(equis) (meanfreq(equis,2500)),deltas_CN,'UniformOutput',false);
y_cn = vertcat(y_cn{:});
y_or_n = cellfun(@(equis) (meanfreq(equis,2500)),deltas_OR_N,'UniformOutput',false);
y_or_n = vertcat(y_or_n{:});
y_or_n_s = cellfun(@(equis) (meanfreq(equis,2500)),deltas_OR_N_S,'UniformOutput',false);
y_or_n_s = vertcat(y_or_n_s{:});
y_or_nn_s = cellfun(@(equis) (meanfreq(equis,2500)),deltas_OR_NN_S,'UniformOutput',false);
y_or_nn_s = vertcat(y_or_nn_s{:});

% Amplitude
z_or = cellfun(@(equis) max(abs(hilbert(equis))) ,deltas_OR,'UniformOutput',false);
z_or = vertcat(z_or{:});
z_hc = cellfun(@(equis) max(abs(hilbert(equis))),deltas_HC,'UniformOutput',false);
z_hc = vertcat(z_hc{:});
z_od = cellfun(@(equis) max(abs(hilbert(equis))) ,deltas_OD,'UniformOutput',false);
z_od = vertcat(z_od{:});
z_cn = cellfun(@(equis) max(abs(hilbert(equis))),deltas_CN,'UniformOutput',false);
z_cn = vertcat(z_cn{:});
z_or_n = cellfun(@(equis) max(abs(hilbert(equis))),deltas_OR_N,'UniformOutput',false);
z_or_n = vertcat(z_or_n{:});
z_or_n_s = cellfun(@(equis) max(abs(hilbert(equis))),deltas_OR_N_S,'UniformOutput',false);
z_or_n_s = vertcat(z_or_n_s{:});
z_or_nn_s = cellfun(@(equis) max(abs(hilbert(equis))),deltas_OR_NN_S,'UniformOutput',false);
z_or_nn_s = vertcat(z_or_nn_s{:});

% Area under curve
l_or = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_OR,'UniformOutput',false));
l_hc = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_HC,'UniformOutput',false));
l_od = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_OD,'UniformOutput',false));
l_cn = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_CN,'UniformOutput',false));
l_or_n = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_OR_N,'UniformOutput',false));
l_or_n_s = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_OR_N_S,'UniformOutput',false));
l_or_nn_s = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), deltas_OR_NN_S,'UniformOutput',false));

% Duration
q_or =(cellfun('length',deltas_OR)/2500);
q_hc = (cellfun('length',deltas_HC)/2500);
q_od =(cellfun('length',deltas_OD)/2500);
q_cn = (cellfun('length',deltas_CN)/2500);
q_or_n = (cellfun('length',deltas_OR_N)/2500);
q_or_n_s = (cellfun('length',deltas_OR_N_S)/2500);
q_or_nn_s = (cellfun('length',deltas_OR_NN_S)/2500);

% PeaktoPeak Amplitude
p_or = cellfun(@peak2peak,deltas_OR);
p_hc = cellfun(@peak2peak,deltas_HC);
p_od = cellfun(@peak2peak,deltas_OD);
p_cn = cellfun(@peak2peak,deltas_CN);
p_or_n = cellfun(@peak2peak,deltas_OR_N);
p_or_n_s = cellfun(@peak2peak,deltas_OR_N_S);
p_or_nn_s = cellfun(@peak2peak,deltas_OR_NN_S);

% Combination of characteristics 
try
l_hc = l_hc';
l_cn = l_cn';
l_od = l_od';
l_or = l_or';
l_or_n = l_or_n';
l_or_n_s = l_or_n_s';
l_or_nn_s = l_or_nn_s';

q_hc = q_hc';
q_cn = q_cn';
q_od = q_od';
q_or = q_or';
q_or_n = q_or_n';
q_or_n_s = q_or_n_s';
q_or_nn_s = q_or_nn_s';

p_hc = p_hc';
p_cn = p_cn';
p_od = p_od';
p_or = p_or';
p_or_n = p_or_n';
p_or_n_s = p_or_n_s';
p_or_nn_s = p_or_nn_s';

totalCharacteristicsHC= [x_hc y_hc z_hc l_hc q_hc p_hc];
totalCharacteristicsCN= [x_cn y_cn z_cn l_cn q_cn p_cn];
totalCharacteristicsOD= [x_od y_od z_od l_od q_od p_od];
totalCharacteristicsOR= [x_or y_or z_or l_or q_or p_or];
totalCharacteristicsOR_N= [x_or_n y_or_n z_or_n l_or_n q_or_n p_or_n];
totalCharacteristicsOR_N_S= [x_or_n_s y_or_n_s z_or_n_s l_or_n_s q_or_n_s p_or_n_s];
totalCharacteristicsOR_NN_S= [x_or_nn_s y_or_nn_s z_or_nn_s l_or_nn_s q_or_nn_s p_or_nn_s];
catch 
totalCharacteristicsHC= [x_hc y_hc z_hc l_hc q_hc p_hc];
totalCharacteristicsCN= [x_cn y_cn z_cn l_cn q_cn p_cn];
totalCharacteristicsOD= [x_od y_od z_od l_od q_od p_od];
totalCharacteristicsOR= [x_or y_or z_or l_or q_or p_or];
totalCharacteristicsOR_N= [x_or_n y_or_n z_or_n l_or_n q_or_n p_or_n];
totalCharacteristicsOR_N_S= [x_or_n_s y_or_n_s z_or_n_s l_or_n_s q_or_n_s p_or_n_s];
totalCharacteristicsOR_NN_S= [x_or_nn_s y_or_nn_s z_or_nn_s l_or_nn_s q_or_nn_s p_or_nn_s];
end

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

