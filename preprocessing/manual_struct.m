%% Manual creation of data struct. 
 
% Dataset  Treatment     RatIDDataset   Condition    Trial
%   CBD      CBD          Rat1CBD          CON      Presleep


%Rat 4
CBD.VEH.Rat4CBD.OR=Z;
CBD.VEH.Rat4CBD.HC=Z;
CBD.CBD.Rat4CBD.OR=Z;
CBD.CBD.Rat4CBD.OD=Z;
CBD.VEH.Rat4CBD.OD=Z;
CBD.CBD.Rat4CBD.HC=Z;
% Rat 5
CBD.CBD.Rat5CBD.OR=Z;
CBD.VEH.Rat5CBD.OR=Z;
CBD.VEH.Rat5CBD.OD=Z;
CBD.VEH.Rat5CBD.HC=Z;
CBD.CBD.Rat5CBD.OD=Z;
CBD.CBD.Rat5CBD.HC=Z;

% Rat 6
CBD.VEH.Rat6CBD.OR=Z;
CBD.CBD.Rat6CBD.OR=Z;
CBD.CBD.Rat6CBD.OD=Z;
CBD.VEH.Rat6CBD.HC=Z;
CBD.VEH.Rat6CBD.OD=Z;
CBD.CBD.Rat6CBD.HC=Z;

clear Z
%%
cd('/mnt/genzel/Rat/OS_UMAP_analysis/UMAP_Basic_OS/1')

load('preprocessed2_GC_window_ripples_broadband_CN.mat')
OSBASIC.VEH.Rat1BASIC.CN=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_HC.mat')
OSBASIC.VEH.Rat1BASIC.HC=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_OD.mat')
OSBASIC.VEH.Rat1BASIC.OD=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_study_day_2_OR.mat')
OSBASIC.VEH.Rat1BASIC.OR=Z;
clear Z


cd('/mnt/genzel/Rat/OS_UMAP_analysis/UMAP_Basic_OS/3')

load('preprocessed2_GC_window_ripples_broadband_CN.mat')
OSBASIC.VEH.Rat3BASIC.CN=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_OD.mat')
OSBASIC.VEH.Rat3BASIC.OD=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_Rat_OS_Ephys_Rat3_SD1_OR_08-09_11_2017.mat')
OSBASIC.VEH.Rat3BASIC.OR=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_Rat_OS_Ephys_Rat3_SD3_HC_15_11_2017.mat')
OSBASIC.VEH.Rat3BASIC.HC=Z;
clear Z


cd('/mnt/genzel/Rat/OS_UMAP_analysis/UMAP_Basic_OS/4')

load('preprocessed2_GC_window_ripples_broadband_CN.mat')
OSBASIC.VEH.Rat4BASIC.CN=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_OD.mat')
OSBASIC.VEH.Rat4BASIC.OD=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_Rat_OS_Ephys_Rat4_SD2_HC_13_12_2017.mat')
OSBASIC.VEH.Rat4BASIC.HC=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_Rat_OS_Ephys_Rat4_SD3_OR_11-12_12_2017.mat')
OSBASIC.VEH.Rat4BASIC.OR=Z;
clear Z

cd('/mnt/genzel/Rat/OS_UMAP_analysis/UMAP_Basic_OS/6')
load('preprocessed2_GC_window_ripples_broadband_CN.mat')
OSBASIC.VEH.Rat6BASIC.CN=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_Study_day1_HC_16feb2018.mat')
OSBASIC.VEH.Rat6BASIC.HC=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_Study_day2_OD_19_20feb2018.mat')
OSBASIC.VEH.Rat6BASIC.OD=Z;
clear Z
load('preprocessed2_GC_window_ripples_broadband_Study_day5_OR_26_27feb2018.mat')
OSBASIC.VEH.Rat6BASIC.OR=Z;
clear Z

%xo
cd('/mnt/genzel/Rat/OS_UMAP_analysis/UMAP_Basic_OS/9')

load('preprocessed2_GC_window_ripples_broadband_2018_06_04_Study_day10_OR.mat')
OSBASIC.VEH.Rat9BASIC.OR=Z;
clear Z

load('preprocessed2_GC_window_ripples_broadband_CN.mat')
OSBASIC.VEH.Rat9BASIC.CN=Z;
clear Z

load('preprocessed2_GC_window_ripples_broadband_HC.mat')
OSBASIC.VEH.Rat9BASIC.HC=Z;
clear Z

load('preprocessed2_GC_window_ripples_broadband_OD.mat')
OSBASIC.VEH.Rat9BASIC.OD=Z;
clear Z

cd('/mnt/genzel/Rat/OS_UMAP_analysis/UMAP_Basic_OS/11')

load('preprocessed2_GC_window_ripples_broadband_CN.mat')
OSBASIC.VEH.Rat11BASIC.CN=Z;
clear Z

load('preprocessed2_GC_window_ripples_broadband_HC.mat')
OSBASIC.VEH.Rat11BASIC.HC=Z;
clear Z

load('preprocessed2_GC_window_ripples_broadband_OD.mat')
OSBASIC.VEH.Rat11BASIC.OD=Z;
clear Z

load('preprocessed2_GC_window_ripples_broadband_OR.mat')
OSBASIC.VEH.Rat11BASIC.OR=Z;
clear Z

cd('/mnt/genzel/Rat/OS_UMAP_analysis/UMAP_Basic_OS/13')

load('preprocessed2_GC_window_ripples_broadband_CN.mat')
OSBASIC.VEH.Rat13BASIC.CN=Z;
clear Z

load('preprocessed2_GC_window_ripples_broadband_Rat_OS_Ephys_Rat13_344994_SD2_HC_15_05_2019.mat')
OSBASIC.VEH.Rat13BASIC.HC=Z;
clear Z

load('preprocessed2_GC_window_ripples_broadband_Rat_OS_Ephys_Rat13_344994_SD3_OR_16-17_05_2019.mat')
OSBASIC.VEH.Rat13BASIC.OR=Z;
clear Z

load('preprocessed2_GC_window_ripples_broadband_Rat_OS_Ephys_Rat13_344994_SD4_OD_21-22_05_2019.mat')
OSBASIC.VEH.Rat13BASIC.OD=Z;
clear Z

%% RGS14

RGS14.VEH.Rat1RGS.CN=Z;
RGS14.VEH.Rat1RGS.OD=Z;
RGS14.VEH.Rat1RGS.OR=Z;
RGS14.VEH.Rat1RGS.HC=Z;


RGS14.VEH.Rat2RGS.OD=Z;
RGS14.VEH.Rat2RGS.OR=Z;
RGS14.VEH.Rat2RGS.CN=Z;
RGS14.VEH.Rat2RGS.HC=Z;

clear Z

RGS14.RGS.Rat3RGS.OD=Z;
RGS14.RGS.Rat3RGS.OR=Z;
RGS14.RGS.Rat3RGS.CN=Z;
RGS14.RGS.Rat3RGS.HC=Z;

clear Z

RGS14.RGS.Rat4RGS.CN=Z;
RGS14.RGS.Rat4RGS.HC=Z;
RGS14.RGS.Rat4RGS.OD=Z;
RGS14.RGS.Rat4RGS.OR=Z;

clear Z

RGS14.VEH.Rat6RGS.HC=Z;
RGS14.VEH.Rat6RGS.OR=Z;
RGS14.VEH.Rat6RGS.CN=Z;
RGS14.VEH.Rat6RGS.OD=Z;

clear Z


RGS14.RGS.Rat7RGS.HC=Z;
RGS14.RGS.Rat7RGS.OR=Z;
RGS14.RGS.Rat7RGS.CN=Z;
RGS14.RGS.Rat7RGS.OD=Z;

clear Z


RGS14.RGS.Rat8RGS.HC=Z;
RGS14.RGS.Rat8RGS.CN=Z;
RGS14.RGS.Rat8RGS.OR=Z;
RGS14.RGS.Rat8RGS.OD=Z;

clear Z

RGS14.VEH.Rat9RGS.HC=Z;
RGS14.VEH.Rat9RGS.CN=Z;
RGS14.VEH.Rat9RGS.OR=Z;
RGS14.VEH.Rat9RGS.OD=Z;

