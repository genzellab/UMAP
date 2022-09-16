%% SAME TRIAL, DIFFERENT CONDITION
clearvars
clc
close all
% x- Entropy; y- Mean Freq; z- Amplitude; l- AUC; q- Duration; p- Peak2Peak
% OR 
% [OR,path]=uigetfile('spindles_waveforms_broadband*.mat','Select OR');
% File=fullfile(path,OR)
% spindles_waveform_broadband_total_OR=load(File);
% spindles_OR_total=spindles_waveform_broadband_total_OR.spindles_waveform_broadband_total;
% 
% % HC
% [HC,path]=uigetfile('spindles_waveforms_broadband*.mat','Select HC');
% File=fullfile(path,HC)
% spindles_waveform_broadband_total_HC=load(File);
% spindles_HC_total=spindles_waveform_broadband_total_HC.spindles_waveform_broadband_total;
% 
% % CN
% [CN,path]=uigetfile('spindles_waveforms_broadband*.mat','Select CN');
% File=fullfile(path,CN)
% spindles_waveform_broadband_total_CN=load(File);
% spindles_CN_total=spindles_waveform_broadband_total_CN.spindles_waveform_broadband_total;
% 
% % OD
% [OD,path]=uigetfile('spindles_waveforms_broadband*.mat','Select OD');
% File=fullfile(path,OD)
% spindles_waveform_broadband_total_OD=load(File);
% spindles_OD_total=spindles_waveform_broadband_total_OD.spindles_waveform_broadband_total;

%cd('/media/genzel/genzel1/UMAP_NSD/6_35/')
cd('/media/genzel/genzel1/UMAP_Basic_OS/9/')
% cd('/media/genzel/genzel1/RGS14_NSD/RGS_Rats/6')

% prompt = {'Select a trial for comparison 1(presleep)-2(PT1)-3(PT2)-4(PT3)-5(PT4)-6(PT5.1)-7(PT5.2)-8(PT5.3)-9(PT5.4))'};
% dlgtitle = 'Choose between (1-9)';
% definput = {'9'};
% ChosenPT = inputdlg(prompt,dlgtitle,[1 80],definput); %Chosen PT for Characteristics
% m=str2double(ChosenPT{1, 1});

m=9; %1(presleep)-2(PT1)-3(PT2)-4(PT3)-5(PT4)-6(PT5.1)-7(PT5.2)-8(PT5.3)-9(PT5.4)

[Conditions,path]=uigetfile('spindles_waveforms_broadband*.mat','MultiSelect','on');

OR=Conditions(find(contains(Conditions,'OR')))
if ~isempty(OR)
FileOR=fullfile(path,OR{1,end})
spindles_waveform_broadband_total_OR=load(FileOR);
spindles_OR_total=spindles_waveform_broadband_total_OR.spindles_waveform_broadband_total;
spindles_OR = spindles_OR_total{1, m}';
else
    spindles_OR = {};
end

HC=Conditions(find(contains(Conditions,'HC')))
if ~isempty(HC)
FileHC=fullfile(path,HC{1,1})
spindles_waveform_broadband_total_HC=load(FileHC);
spindles_HC_total=spindles_waveform_broadband_total_HC.spindles_waveform_broadband_total;
spindles_HC = spindles_HC_total{1, m}';
else
    spindles_HC={}; 
end

CN=Conditions(find(contains(Conditions,'CN')))
if ~isempty(CN)
FileCN=fullfile(path,CN{1,1})
spindles_waveform_broadband_total_CN=load(FileCN);
spindles_CN_total=spindles_waveform_broadband_total_CN.spindles_waveform_broadband_total;
spindles_CN = spindles_CN_total{1, m}';
else
    spindles_CN={}; 
end

OD=Conditions(find(contains(Conditions,'OD')))
if ~isempty(OD)
FileOD=fullfile(path,OD{1,1})
spindles_waveform_broadband_total_OD=load(FileOD);
spindles_OD_total=spindles_waveform_broadband_total_OD.spindles_waveform_broadband_total;
spindles_OD = spindles_OD_total{1, m}';
else
    spindles_OD={}; 
end

OR_N=Conditions(find(contains(Conditions,'OR_N')))
if ~isempty(OR_N)
FileOR_N=fullfile(path,OR_N{1,1})
spindles_waveform_broadband_total_OR_N=load(FileOR_N);
spindles_OR_N_total=spindles_waveform_broadband_total_OR_N.spindles_waveform_broadband_total;
spindles_OR_N = spindles_OR_N_total{1, m}';
else
    spindles_OR_N={}; 
end

OR_N_S=Conditions(find(contains(Conditions,'OR_N_S')))
if ~isempty(OR_N_S)
FileOR_N_S=fullfile(path,OR_N_S{1,1})
spindles_waveform_broadband_total_OR_N_S=load(FileOR_N_S);
spindles_OR_N_S_total=spindles_waveform_broadband_total_OR_N_S.spindles_waveform_broadband_total;
spindles_OR_N_S = spindles_OR_N_S_total{1, m}';
else
    spindles_OR_N_S={}; 
end

OR_NN_S=Conditions(find(contains(Conditions,'OR_NN_S')))
if ~isempty(OR_NN_S)
FileOR_NN_S=fullfile(path,OR_NN_S{1,1})
spindles_waveform_broadband_total_OR_NN_S=load(FileOR_NN_S);
spindles_OR_NN_S_total=spindles_waveform_broadband_total_OR_NN_S.spindles_waveform_broadband_total;
spindles_OR_NN_S = spindles_OR_NN_S_total{1, m}';
else
    spindles_OR_NN_S={}; 
end

if ~iscell(spindles_HC)
    if isnan(spindles_HC)
        spindles_HC={};
    elseif isempty(spindles_HC)
        spindles_HC={};
    end
end

if ~iscell(spindles_OR)
    if isnan(spindles_OR)
        spindles_OR={};
    elseif isempty(spindles_OR)
        spindles_OR={};
    end
end

if ~iscell(spindles_OD)
    if isnan(spindles_OD)
        spindles_OD={};
    elseif isempty(spindles_OD)
        spindles_OD={};
    end
end

if ~iscell(spindles_CN)
    if isnan(spindles_CN)
        spindles_CN={};
    elseif isempty(spindles_CN)
        spindles_CN={};
    end
end

if ~iscell(spindles_OR_N)
    if isnan(spindles_OR_N)
        spindles_OR_N={};
    elseif isempty(spindles_OR_N)
        spindles_OR_N={};
    end
end

if ~iscell(spindles_OR_N_S)
    if isnan(spindles_OR_N_S)
        spindles_OR_N_S={};
    elseif isempty(spindles_OR_N_S)
        spindles_OR_N_S={};
    end
end

if ~iscell(spindles_OR_NN_S)
    if isnan(spindles_OR_NN_S)
        spindles_OR_NN_S={};
    elseif isempty(spindles_OR_NN_S)
        spindles_OR_NN_S={};
    end
end


si_index = cellfun(@(equis) sum(isnan(equis)), spindles_HC,'UniformOutput',false);
si_index= cell2mat(si_index);
si_index = ~logical(si_index);
spindles_HC= spindles_HC(si_index);

si_index = cellfun(@(equis) sum(isnan(equis)), spindles_OR,'UniformOutput',false);
si_index = cell2mat(si_index);
si_index = ~logical(si_index);
spindles_OR = spindles_OR(si_index); 

si_index = cellfun(@(equis) sum(isnan(equis)), spindles_OD,'UniformOutput',false);
si_index= cell2mat(si_index);
si_index = ~logical(si_index);
spindles_OD= spindles_OD(si_index);

si_index = cellfun(@(equis) sum(isnan(equis)), spindles_CN,'UniformOutput',false);
si_index = cell2mat(si_index);
si_index = ~logical(si_index);
spindles_CN = spindles_CN(si_index); 

si_index = cellfun(@(equis) sum(isnan(equis)), spindles_OR_N,'UniformOutput',false);
si_index= cell2mat(si_index);
si_index = ~logical(si_index);
spindles_OR_N= spindles_OR_N(si_index);

si_index = cellfun(@(equis) sum(isnan(equis)), spindles_OR_N_S,'UniformOutput',false);
si_index= cell2mat(si_index);
si_index = ~logical(si_index);
spindles_OR_N_S= spindles_OR_N_S(si_index);

si_index = cellfun(@(equis) sum(isnan(equis)), spindles_OR_NN_S,'UniformOutput',false);
si_index= cell2mat(si_index);
si_index = ~logical(si_index);
spindles_OR_NN_S= spindles_OR_NN_S(si_index);



Wn1=[100/(2500/2) 300/(2500/2)]; % Cutoff=100-300 Hz
[b1,a1] = butter(3,Wn1,'bandpass'); %Filter coefficients
spindles_OR = cellfun(@(equis)filtfilt(b1,a1,equis),spindles_OR ,'UniformOutput',false);
spindles_HC = cellfun(@(equis)filtfilt(b1,a1,equis),spindles_HC ,'UniformOutput',false);
spindles_OD = cellfun(@(equis)filtfilt(b1,a1,equis),spindles_OD ,'UniformOutput',false);
spindles_CN = cellfun(@(equis)filtfilt(b1,a1,equis),spindles_CN ,'UniformOutput',false);
spindles_OR_N = cellfun(@(equis)filtfilt(b1,a1,equis),spindles_OR_N ,'UniformOutput',false);
spindles_OR_N_S = cellfun(@(equis)filtfilt(b1,a1,equis),spindles_OR_N_S ,'UniformOutput',false);
spindles_OR_NN_S = cellfun(@(equis)filtfilt(b1,a1,equis),spindles_OR_NN_S ,'UniformOutput',false);

% Entropy
x_or = cellfun(@(equis) entropy(equis),spindles_OR,'UniformOutput',false);
x_or = vertcat(x_or{:});
x_hc = cellfun(@(equis) entropy(equis),spindles_HC,'UniformOutput',false);
x_hc = vertcat(x_hc{:});
x_od = cellfun(@(equis) entropy(equis),spindles_OD,'UniformOutput',false);
x_od = vertcat(x_od{:});
x_cn = cellfun(@(equis) entropy(equis),spindles_CN,'UniformOutput',false);
x_cn = vertcat(x_cn{:});
x_or_n = cellfun(@(equis) entropy(equis),spindles_OR_N,'UniformOutput',false);
x_or_n = vertcat(x_or_n{:});
x_or_n_s = cellfun(@(equis) entropy(equis),spindles_OR_N_S,'UniformOutput',false);
x_or_n_s = vertcat(x_or_n_s{:});
x_or_nn_s = cellfun(@(equis) entropy(equis),spindles_OR_NN_S,'UniformOutput',false);
x_or_nn_s = vertcat(x_or_nn_s{:});

% Mean Freqs
y_or = cellfun(@(equis) (meanfreq(equis,2500)),spindles_OR,'UniformOutput',false);
y_or = vertcat(y_or{:});
y_hc = cellfun(@(equis) (meanfreq(equis,2500)),spindles_HC,'UniformOutput',false);
y_hc = vertcat(y_hc{:});
y_od = cellfun(@(equis) (meanfreq(equis,2500)),spindles_OD,'UniformOutput',false);
y_od = vertcat(y_od{:});
y_cn = cellfun(@(equis) (meanfreq(equis,2500)),spindles_CN,'UniformOutput',false);
y_cn = vertcat(y_cn{:});
y_or_n = cellfun(@(equis) (meanfreq(equis,2500)),spindles_OR_N,'UniformOutput',false);
y_or_n = vertcat(y_or_n{:});
y_or_n_s = cellfun(@(equis) (meanfreq(equis,2500)),spindles_OR_N_S,'UniformOutput',false);
y_or_n_s = vertcat(y_or_n_s{:});
y_or_nn_s = cellfun(@(equis) (meanfreq(equis,2500)),spindles_OR_NN_S,'UniformOutput',false);
y_or_nn_s = vertcat(y_or_nn_s{:});

% Amplitude
z_or = cellfun(@(equis) max(abs(hilbert(equis))) ,spindles_OR,'UniformOutput',false);
z_or = vertcat(z_or{:});
z_hc = cellfun(@(equis) max(abs(hilbert(equis))),spindles_HC,'UniformOutput',false);
z_hc = vertcat(z_hc{:});
z_od = cellfun(@(equis) max(abs(hilbert(equis))) ,spindles_OD,'UniformOutput',false);
z_od = vertcat(z_od{:});
z_cn = cellfun(@(equis) max(abs(hilbert(equis))),spindles_CN,'UniformOutput',false);
z_cn = vertcat(z_cn{:});
z_or_n = cellfun(@(equis) max(abs(hilbert(equis))),spindles_OR_N,'UniformOutput',false);
z_or_n = vertcat(z_or_n{:});
z_or_n_s = cellfun(@(equis) max(abs(hilbert(equis))),spindles_OR_N_S,'UniformOutput',false);
z_or_n_s = vertcat(z_or_n_s{:});
z_or_nn_s = cellfun(@(equis) max(abs(hilbert(equis))),spindles_OR_NN_S,'UniformOutput',false);
z_or_nn_s = vertcat(z_or_nn_s{:});


% Area under curve
l_or = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), spindles_OR,'UniformOutput',false));
l_hc = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), spindles_HC,'UniformOutput',false));
l_od = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), spindles_OD,'UniformOutput',false));
l_cn = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), spindles_CN,'UniformOutput',false));
l_or_n = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), spindles_OR_N,'UniformOutput',false));
l_or_n_s = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), spindles_OR_N_S,'UniformOutput',false));
l_or_nn_s = cell2mat(cellfun(@(equis) trapz((1:length(equis))./2500,abs(equis)), spindles_OR_NN_S,'UniformOutput',false));

% Duration
q_or =(cellfun('length',spindles_OR)/2500);
q_hc = (cellfun('length',spindles_HC)/2500);
q_od =(cellfun('length',spindles_OD)/2500);
q_cn = (cellfun('length',spindles_CN)/2500);
q_or_n = (cellfun('length',spindles_OR_N)/2500);
q_or_n_s = (cellfun('length',spindles_OR_N_S)/2500);
q_or_nn_s = (cellfun('length',spindles_OR_NN_S)/2500);

% PeaktoPeak Amplitude
p_or = cellfun(@peak2peak,spindles_OR);
p_hc = cellfun(@peak2peak,spindles_HC);
p_od = cellfun(@peak2peak,spindles_OD);
p_cn = cellfun(@peak2peak,spindles_CN);
p_or_n = cellfun(@peak2peak,spindles_OR_N);
p_or_n_s = cellfun(@peak2peak,spindles_OR_N_S);
p_or_nn_s = cellfun(@peak2peak,spindles_OR_NN_S);

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

% l_hc = l_hc';
% l_cn = l_cn';
% l_od = l_od';
% l_or = l_or';

% q_hc = q_hc';
% q_cn = q_cn';
% q_od = q_od';
% q_or = q_or';

% p_hc = p_hc';
% p_cn = p_cn';
% p_od = p_od';
% p_or = p_or';

% totalCharacteristicsHC= [x_hc y_hc z_hc l_hc q_hc p_hc];
% totalCharacteristicsCN= [x_cn y_cn z_cn l_cn q_cn p_cn];
% totalCharacteristicsOD= [x_od y_od z_od l_od q_od p_od];
% totalCharacteristicsOR= [x_or y_or z_or l_or q_or p_or];
