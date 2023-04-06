#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 12:38:57 2022

@author: adrian
"""

import os
import sys
# TODO: Select path wrt your system
#os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');
os.chdir('/mnt/genzel/Rat/OS_CBD_analysis/chronic')
#os.chdir('/home/blazkowiz47/work/UMAP/dataset');
# sys.path.append('/home/genzel/Documents/UMAP')

import scipy.io
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cl

from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import cv2
import umap
#import plotly.express as px
from URC_computeIsomapDimEst import isomapDimEst
import utils.plotting_helpers as hplt
import utils.processing_helpers as hproc
from sklearn.cluster import KMeans, DBSCAN
from seaborn import kdeplot
import pickle


sns.set(style='white',context='poster', rc={'figure.figsize':(14,10)} )
# %% Load whole table and split columns 
### Start Loading data


#Includes ripples from all datasets
myDict = scipy.io.loadmat('Tcell_17_01_2023.mat')
T=myDict['T_cell']

#CBD dataset
myDict = scipy.io.loadmat('Tcell_cbd_17_01_2023.mat')
T_cbd=myDict['Tcell']

#RGS dataset
myDict = scipy.io.loadmat('Tcell_RGS14_03_12_2022.mat')
T_rgs=myDict['Tcell_RGS14_03_12_2022']

#OS Basic dataset
myDict = scipy.io.loadmat('Tcell_OSBASIC_17_01_2023.mat')
T_osbasic=myDict['Tcell']

#We use T which contains data from all datasets. 

#Ripples waveforms
Ripples=T[:,5]
Data = hproc.v_stack(Ripples[2:]) #Number of ripples by 127
#Dataset label
#dataset_np=T[:,0]
dataset_rip=hproc.unfold_days2ripples(Ripples,T[:,0])
#Treatment
#treatment_np=T[:,1]
treatment_rip=hproc.unfold_days2ripples(Ripples,T[:,1])
#Rat
#rat_np=T[:,2]
rat_rip=hproc.unfold_days2ripples(Ripples, T[:,2])
#StudyDay
#StudyDay_np=T[:,3]
StudyDay_rip=hproc.unfold_days2ripples(Ripples, T[:,3])
#Trial
#trial_np=T[:,4]
trial_rip=hproc.unfold_days2ripples(Ripples,T[:,4])

#Amplitude
amplitude_np=T[:,6];
#Meanfreq
meanfreq_np=T[:,7];
#Duration
duration_np=T[:,8];
#Phase
phase_np=T[:,9];
# SO power before
so_before_np=T[:,10];
# SO power after
so_after_np=T[:,11];
# Spectral entropy
s_entropy_np=T[:,13];


#Features per ripple    
Amp=hproc.flatcells(amplitude_np[2:]);
Meanfreq=hproc.flatcells(meanfreq_np[2:]);

Duration=hproc.flatcells(duration_np[2:]);
Phase=hproc.flatcells(phase_np[2:]);

SO_before=hproc.flatcells(so_before_np[2:]);
SO_after=hproc.flatcells(so_after_np[2:]);

S_entropy=hproc.flatcells(s_entropy_np[2:]);


#Separate datasets: T_cbd, T_rgs, T_osbasic. (Split for sanite check, ideally just use T)

Ripples_cbd=T_cbd[:,5]
Ripples_cbd=Ripples_cbd[2:];
Data_cbd = hproc.v_stack(Ripples_cbd)

Ripples_rgs=T_rgs[:,5]
Data_rgs = hproc.v_stack(Ripples_rgs)
treatment_np_rgs=T_rgs[:,1]
treatment_rip_rgs=hproc.unfold_days2ripples(Ripples_rgs,treatment_np_rgs)


Ripples_osbasic=T_osbasic[:,5]
Data_osbasic = hproc.v_stack(Ripples_osbasic)

# %%  Compute UMAP from Data (T)
fit = umap.UMAP(n_components=4)
u=fit.fit_transform(Data)
# Compute from split datasets. 
u_cbd = fit.fit_transform(Data_cbd)
u_rgs = fit.fit_transform(Data_rgs)
u_osbasic = fit.fit_transform(Data_osbasic)

# %% Figures, describing embeddings.
# def cm2inch(value):
#     return value/2.54
# figsize=(cm2inch(3.5), cm2inch(3.5))
# plt.figure(figsize=(cm2inch(12.8), cm2inch(9.6)))


# %% Looking for outliers
#Density
hplt.plot3Ddensity(u_rgs[:,0],u_rgs[:,1],u_rgs[:,2], zlabel='umap 3', bins=50)

hplt.plot3Ddensity(u_cbd[:,0],u_cbd[:,1],u_cbd[:,3], zlabel='umap 4', bins=50)

hplt.plot3Ddensity(u_osbasic[:,0],u_osbasic[:,1],u_osbasic[:,2], zlabel='umap 3', bins=50)


hplt.plot3Ddensity(u[:,0],u[:,1],u[:,3], zlabel='umap 4', bins=50)

# %% Remove outliers using DBSCAN clustering.

[outliers_osbasic]=hproc.dbscan_outliers(u_osbasic, "OS_basic", eps_value=0.2, min_samples_value=10, outlier_label=1)
[outliers_rgs]=hproc.dbscan_outliers(u_rgs, "RGS14", eps_value=0.2, min_samples_value=10, outlier_label=1)
[outliers_cbd]=hproc.dbscan_outliers(u_cbd, "CBD", eps_value=0.10, min_samples_value=1, outlier_label=1)
[outliers]=hproc.dbscan_outliers(u, "Combined", eps_value=0.2, min_samples_value=5, outlier_label=1)

#[:,0:2]
# %% Using combined outliers from all datasets. 
outliers_combined=np.concatenate([outliers_cbd,outliers_osbasic,outliers_rgs]);

# Remove outliers from features data. 
Meanfreq_combined=Meanfreq[np.logical_not(outliers_combined)];
Amp_combined=Amp[np.logical_not(outliers_combined)];

Duration_combined=Duration[np.logical_not(outliers_combined)];
Phase_combined=Phase[np.logical_not(outliers_combined)];

SO_before_combined=SO_before[np.logical_not(outliers_combined)];
SO_after_combined=SO_after[np.logical_not(outliers_combined)];

S_entropy_combined=S_entropy[np.logical_not(outliers_combined)];

# %% Re compute UMAP without outliers

fit = umap.UMAP(n_components=4)
Data_clean=Data[np.logical_not(outliers_combined)];
u_clean=fit.fit_transform(Data[np.logical_not(outliers_combined)])
u_cbd_clean = fit.fit_transform(Data_cbd[np.logical_not(outliers_cbd)])
u_rgs_clean = fit.fit_transform(Data_rgs[np.logical_not(outliers_rgs)])
u_osbasic_clean = fit.fit_transform(Data_osbasic[np.logical_not(outliers_osbasic)])


# %% Figures, describing embeddings. Per dataset. Without outliers 
# def cm2inch(value):
#     return value/2.54
# figsize=(cm2inch(3.5), cm2inch(3.5))
# plt.figure(figsize=(cm2inch(12.8), cm2inch(9.6)))
list_colours=['#0343DF','#E50000','#15B01A','black'];
list_embeddings=[u_rgs_clean,u_osbasic_clean,u_cbd_clean,u_clean];
list_names=["RGS14 dataset","OS basic dataset", "CBD dataset","Combined datasets"]

for (item,colours,names) in zip(list_embeddings, list_colours,list_names):
    hplt.plot_scatter(item[:,0],item[:,1] ,title=names,s=1,xlabel='Umap 1',ylabel='Umap 2',c=colours)
    plt.xlim([-1,11])
    plt.ylim([-1,11])

#%% Store outliers in Dataframe
df = pd.DataFrame(dataset_rip[outliers_combined], columns = ['Dataset'])
df['Treatment'] = treatment_rip[outliers_combined]
df['Rat'] = rat_rip[outliers_combined]
df['StudyDay'] = StudyDay_rip[outliers_combined]
df['Trial'] = trial_rip[outliers_combined]

df.to_csv('outliers.csv')  
#%%
#%% Split by treatment, not by dataset.
treatment_veh=hproc.strcmp(treatment_rip,"VEH") #OSBASIC #RGS14
treatment_cbd=hproc.strcmp(treatment_rip,"CBD") #OSBASIC #RGS14
treatment_rgs=hproc.strcmp(treatment_rip,"RGS") #OSBASIC #RGS14


Data_veh_treatment=Data[np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))]
Data_cbd_treatment=Data[np.logical_and(np.squeeze(treatment_cbd)==1,np.logical_not(outliers_combined))]
Data_rgs_treatment=Data[np.logical_and(np.squeeze(treatment_rgs)==1,np.logical_not(outliers_combined))]


fit = umap.UMAP(n_components=4)
u_cbd_treatment = fit.fit_transform(Data_cbd_treatment)
u_rgs_treatment = fit.fit_transform(Data_rgs_treatment)
u_veh_treatment = fit.fit_transform(Data_veh_treatment)



#%%
list_colours=['#0343DF','#E50000','#15B01A','black'];
list_embeddings=[u_rgs_treatment,u_veh_treatment,u_cbd_treatment,u_clean];
list_names=["RGS14 treatment","Vehicle treatment", "CBD treatment","Combined treatment"]

for (item,colours,names) in zip(list_embeddings, list_colours,list_names):
    #ax = fig.add_subplot()
    hplt.plot_scatter(item[:,0],item[:,1] ,title=names,s=1,xlabel='Umap 1',ylabel='Umap 2',c=colours)
    plt.xlim([-1,11])
    plt.ylim([-1,11])


# %%
hplt.plot3Ddensity(u_rgs_treatment[:,0],u_rgs_treatment[:,1],u_rgs_treatment[:,2], zlabel='umap 3', bins=50)

hplt.plot3Ddensity(u_cbd_treatment[:,0],u_cbd_treatment[:,1],u_cbd_treatment[:,2], zlabel='umap 3', bins=50)

hplt.plot3Ddensity(u_veh_treatment[:,0],u_veh_treatment[:,1],u_veh_treatment[:,2], zlabel='umap 3', bins=50)

hplt.plot3Ddensity(u_clean[:,0],u_clean[:,1],u_clean[:,2], zlabel='umap 3', bins=50)

# %% Splitting controls.

dataset_osbasic=hproc.strcmp(dataset_rip,"OSBASIC") #OSBASIC
dataset_cbd=hproc.strcmp(dataset_rip,"CBDchronic") #CBD
dataset_rgs=hproc.strcmp(dataset_rip,"RGS14") #RGS14

#Controls
Data_veh_osbasic_dataset=Data[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_osbasic)==1)]
Data_veh_rgs_dataset=Data[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
Data_veh_cbd_dataset=Data[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

#Non-Controls:
Data_rgs_rgs_dataset=Data[np.logical_and(    np.logical_and(np.squeeze(treatment_rgs)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
Data_cbd_cbd_dataset=Data[np.logical_and(    np.logical_and(np.squeeze(treatment_cbd)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]
    
# All combined except RGS.

Data_combined_no_rgs=np.concatenate([Data_veh_cbd_dataset,Data_cbd_cbd_dataset,Data_veh_osbasic_dataset]);


fit = umap.UMAP(n_components=4)
# Controls
u_veh_osbasic = fit.fit_transform(Data_veh_osbasic_dataset)
u_veh_rgs = fit.fit_transform(Data_veh_rgs_dataset)
u_veh_cbd = fit.fit_transform(Data_veh_cbd_dataset)
# Non-controls
u_rgs_rgs = fit.fit_transform(Data_rgs_rgs_dataset)
u_cbd_cbd = fit.fit_transform(Data_cbd_cbd_dataset)


u_rgs_rgs.shape[0]+u_veh_rgs.shape[0]+u_cbd_cbd.shape[0]+u_veh_cbd.shape[0]+u_veh_osbasic.shape[0]

u_combined_no_rgs = fit.fit_transform(Data_combined_no_rgs)


# %% Plot all embeddings for controls and treatments

plt.rc('font', size=35)
plt.rc('axes', titlesize=35, labelsize=35)

list_colours=['#E50000','purple','saddlebrown','#15B01A','#0343DF','black','gold'];
list_embeddings=[u_veh_osbasic,u_veh_rgs,u_veh_cbd,u_cbd_cbd,u_rgs_rgs,u_clean,u_combined_no_rgs];
list_names=["OS Basic","VEH treatment-RGS dataset", "VEH treatment-CBD dataset","CBD treatment-CBD dataset","RGS treatment-RGS dataset","Combined","Combined (no RGS dataset)"]

for (item,colours,names) in zip(list_embeddings, list_colours,list_names):
    hplt.plot_scatter(item[:,0],item[:,1] ,title=names,s=1,xlabel='Umap 1',ylabel='Umap 2',c=colours)
    plt.xlim([-1,11])
    plt.ylim([-1,11])

# %% Saving embeddings/ Data.

# Saving embeddings:
list_embeddings=[u_veh_osbasic,u_veh_rgs,u_veh_cbd,u_cbd_cbd,u_rgs_rgs,u_clean,u_combined_no_rgs];
with open('embeddings.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(list_embeddings, f)


# Saving data:
list_data=[Data_veh_osbasic_dataset,Data_veh_rgs_dataset,Data_veh_cbd_dataset,Data_cbd_cbd_dataset,Data_rgs_rgs_dataset,Data_clean,Data_combined_no_rgs];
with open('Data.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(list_data, f)
    
# # Getting back the objects:
with open('embeddings.pkl','rb') as f:  # Python 3: open(..., 'rb')
    embeddings= pickle.load(f)    

u_veh_osbasic=embeddings[0];
u_veh_rgs=embeddings[1];
u_veh_cbd=embeddings[2];
u_cbd_cbd=embeddings[3];
u_rgs_rgs=embeddings[4];
u_clean=embeddings[5];
u_combined_no_rgs=embeddings[6];


#,u_veh_rgs,u_veh_cbd,u_cbd_cbd,u_rgs_rgs,u_clean,u_combined_no_rgs];
with open('Data.pkl','rb') as f:  # Python 3: open(..., 'rb')
    Data= pickle.load(f)    

Data_veh_osbasic_dataset=Data[0];
Data_veh_rgs_dataset=Data[1];
Data_veh_cbd_dataset=Data[2];
Data_cbd_cbd_dataset=Data[3];
Data_rgs_rgs_dataset=Data[4];
Data_clean=Data[5];
Data_combined_no_rgs=Data[6];



# %% RGSs

# hplt.plot_umap_binary(u_veh_rgs[:,0],u_veh_rgs[:,1] ,title="VEH RGS",s=1,xlabel='Umap 1',ylabel='Umap 2',c='#0343DF')
# plt.xlim([-1,11])
# plt.ylim([-1,11])

# #u_rgs_treatment
# hplt.plot_umap_binary(u_rgs_treatment[:,0],u_rgs_treatment[:,1] ,title="RGS treatment",s=1,xlabel='Umap 1',ylabel='Umap 2',c='#0343DF')
# plt.xlim([-1,11])
# plt.ylim([-1,11])

# hplt.plot3Ddensity(u_veh_rgs[:,0],u_veh_rgs[:,1],u_veh_rgs[:,2], zlabel='umap 3', bins=50)
# hplt.plot3Ddensity(u_rgs_treatment[:,0],u_rgs_treatment[:,1],u_rgs_treatment[:,2], zlabel='umap 3', bins=50)

# %%
# D_rgs_veh=Data_rgs[np.squeeze(treatment_rip_rgs=='VEH')];

# D_rgs_rgs=Data_rgs[np.squeeze(treatment_rip_rgs=='RGS')];


# fit = umap.UMAP(n_components=4)
# u_rgs_veh = fit.fit_transform(D_rgs_veh)
# u_rgs_rgs = fit.fit_transform(D_rgs_rgs)

# hplt.plot_umap_binary(u_rgs_veh[:,0],u_rgs_veh[:,1] ,title="RGS VEH",s=1,xlabel='Umap 1',ylabel='Umap 2',c='#0343DF')
# plt.xlim([-1,11])
# plt.ylim([-1,11])

# hplt.plot_umap_binary(u_rgs_rgs[:,0],u_rgs_rgs[:,1] ,title="RGS RGS",s=1,xlabel='Umap 1',ylabel='Umap 2',c='#0343DF')
# plt.xlim([-1,11])
# plt.ylim([-1,11])
# %% Displaying features in embedding.
Meanfreq_veh_osbasic_dataset=Meanfreq[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_osbasic)==1)]
Meanfreq_veh_rgs_dataset=Meanfreq[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
Meanfreq_veh_cbd_dataset=Meanfreq[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

#Non-Controls:
Meanfreq_rgs_rgs_dataset=Meanfreq[np.logical_and(    np.logical_and(np.squeeze(treatment_rgs)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
Meanfreq_cbd_cbd_dataset=Meanfreq[np.logical_and(    np.logical_and(np.squeeze(treatment_cbd)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

Meanfreq_combined_no_rgs=np.concatenate([Meanfreq_veh_cbd_dataset,Meanfreq_cbd_cbd_dataset,Meanfreq_veh_osbasic_dataset]);


hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = Meanfreq_veh_osbasic_dataset, title='Veh OS Basic',clipmin=100,clipmax=200)
hplt.plot_umap(x=u_veh_rgs[:,0],y=u_veh_rgs[:,1],feature = Meanfreq_veh_rgs_dataset, title='Veh treatment- RGS dataset',clipmin=100,clipmax=200)
hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = Meanfreq_veh_cbd_dataset, title='Veh treatment- CBD dataset',clipmin=100,clipmax=200)
hplt.plot_umap(x=u_rgs_rgs[:,0],y=u_rgs_rgs[:,1],feature = Meanfreq_rgs_rgs_dataset, title='RGS treatment- RGS dataset',clipmin=100,clipmax=200)
hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = Meanfreq_cbd_cbd_dataset,title='CBD treatment- CBD dataset',clipmin=100,clipmax=200)
hplt.plot_umap(x=u_clean[:,0],y=u_clean[:,1],feature = Meanfreq_combined,title='Combined',clipmin=100,clipmax=200)
hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = Meanfreq_combined_no_rgs,title='Combined (No RGS)',clipmin=100,clipmax=200)



# Saving embeddings:
list_Meanfreq=[Meanfreq_veh_osbasic_dataset,Meanfreq_veh_cbd_dataset,Meanfreq_cbd_cbd_dataset,Meanfreq_combined,Meanfreq_combined_no_rgs];
with open('Meanfreq.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(list_Meanfreq, f)

# # Getting back the objects:
with open('Meanfreq.pkl','rb') as f:  # Python 3: open(..., 'rb')
    Meanfreq_list= pickle.load(f)    

Meanfreq_veh_osbasic_dataset=Meanfreq_list[0];
Meanfreq_veh_cbd_dataset=Meanfreq_list[1];
Meanfreq_cbd_cbd_dataset=Meanfreq_list[2];
Meanfreq_combined=Meanfreq_list[3];
Meanfreq_combined_no_rgs=Meanfreq_list[4];


def structureindex(u,feature,Vmin,Vmax,StringDim1, StringDim2):
    df=pd.DataFrame(u, columns=['u1','u2','u3','u4'])    
    cI_val, bLab, _=URC_computeClusterIndex_V4.computeClusterIndex_V4(df,feature,10,[StringDim1,StringDim2],plotCluster=0,vmin=Vmin, vmax=Vmax)
    return cI_val

si_Meanfreq_u_veh_osbasic_u1_u2=structureindex(u_veh_osbasic,Meanfreq_veh_osbasic_dataset,100,300,'u1', 'u2')
# %%
Amp_veh_osbasic_dataset=Amp[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_osbasic)==1)]
Amp_veh_rgs_dataset=Amp[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
Amp_veh_cbd_dataset=Amp[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

#Non-Controls:
Amp_rgs_rgs_dataset=Amp[np.logical_and(    np.logical_and(np.squeeze(treatment_rgs)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
Amp_cbd_cbd_dataset=Amp[np.logical_and(    np.logical_and(np.squeeze(treatment_cbd)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

Amp_combined_no_rgs=np.concatenate([Amp_veh_cbd_dataset,Amp_cbd_cbd_dataset,Amp_veh_osbasic_dataset]);


hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = Amp_veh_osbasic_dataset, title='Veh OS Basic',clipmin=0,clipmax=4.5)
hplt.plot_umap(x=u_veh_rgs[:,0],y=u_veh_rgs[:,1],feature = Amp_veh_rgs_dataset, title='Veh treatment- RGS dataset',clipmin=0,clipmax=4.5)
hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = Amp_veh_cbd_dataset, title='Veh treatment- CBD dataset',clipmin=0,clipmax=4.5)
hplt.plot_umap(x=u_rgs_rgs[:,0],y=u_rgs_rgs[:,1],feature = Amp_rgs_rgs_dataset, title='RGS treatment- RGS dataset',clipmin=0,clipmax=4.5)
hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = Amp_cbd_cbd_dataset,title='CBD treatment- CBD dataset',clipmin=0,clipmax=4.5)
hplt.plot_umap(x=u_clean[:,0],y=u_clean[:,1],feature = Amp_combined,title='Combined',clipmin=0,clipmax=4.5)
hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = Amp_combined_no_rgs,title='Combined (No RGS)',clipmin=0,clipmax=4.5)

# %%
Duration_veh_osbasic_dataset=Duration[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_osbasic)==1)]
Duration_veh_rgs_dataset=Duration[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
Duration_veh_cbd_dataset=Duration[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

#Non-Controls:
Duration_rgs_rgs_dataset=Duration[np.logical_and(    np.logical_and(np.squeeze(treatment_rgs)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
Duration_cbd_cbd_dataset=Duration[np.logical_and(    np.logical_and(np.squeeze(treatment_cbd)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

Duration_combined_no_rgs=np.concatenate([Duration_veh_cbd_dataset,Duration_cbd_cbd_dataset,Duration_veh_osbasic_dataset]);


hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = Duration_veh_osbasic_dataset, title='Veh OS Basic',clipmin=0,clipmax=100)
#hplt.plot_umap(x=u_veh_rgs[:,0],y=u_veh_rgs[:,1],feature = Duration_veh_rgs_dataset, title='Veh treatment- RGS dataset',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = Duration_veh_cbd_dataset, title='Veh treatment- CBD dataset',clipmin=0,clipmax=100)
#hplt.plot_umap(x=u_rgs_rgs[:,0],y=u_rgs_rgs[:,1],feature = Duration_rgs_rgs_dataset, title='RGS treatment- RGS dataset',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = Duration_cbd_cbd_dataset,title='CBD treatment- CBD dataset',clipmin=0,clipmax=100)
#hplt.plot_umap(x=u_clean[:,0],y=u_clean[:,1],feature = Duration_combined,title='Combined',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = Duration_combined_no_rgs,title='Combined (No RGS)',clipmin=0,clipmax=100)
# %%
Phase_veh_osbasic_dataset=Phase[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_osbasic)==1)]
Phase_veh_rgs_dataset=Phase[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
Phase_veh_cbd_dataset=Phase[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

#Non-Controls:
Phase_rgs_rgs_dataset=Phase[np.logical_and(    np.logical_and(np.squeeze(treatment_rgs)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
Phase_cbd_cbd_dataset=Phase[np.logical_and(    np.logical_and(np.squeeze(treatment_cbd)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

Phase_combined_no_rgs=np.concatenate([Phase_veh_cbd_dataset,Phase_cbd_cbd_dataset,Phase_veh_osbasic_dataset]);


hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = Phase_veh_osbasic_dataset, title='Veh OS Basic',clipmin=0,clipmax=360,cmap='twilight')
#hplt.plot_umap(x=u_veh_rgs[:,0],y=u_veh_rgs[:,1],feature = Phase_veh_rgs_dataset, title='Veh treatment- RGS dataset',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = Phase_veh_cbd_dataset, title='Veh treatment- CBD dataset',clipmin=0,clipmax=360,cmap='twilight')
#hplt.plot_umap(x=u_rgs_rgs[:,0],y=u_rgs_rgs[:,1],feature = Phase_rgs_rgs_dataset, title='RGS treatment- RGS dataset',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = Phase_cbd_cbd_dataset,title='CBD treatment- CBD dataset',clipmin=0,clipmax=360,cmap='twilight')
#hplt.plot_umap(x=u_clean[:,0],y=u_clean[:,1],feature = Phase_combined,title='Combined',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = Phase_combined_no_rgs,title='Combined (No RGS)',clipmin=0,clipmax=360,cmap='twilight')
# %%
from scipy import stats
#SO_before=stats.zscore(SO_before)

SO_before_veh_osbasic_dataset=SO_before[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_osbasic)==1)]
SO_before_veh_rgs_dataset=SO_before[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
SO_before_veh_cbd_dataset=SO_before[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

#Non-Controls:
SO_before_rgs_rgs_dataset=SO_before[np.logical_and(    np.logical_and(np.squeeze(treatment_rgs)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
SO_before_cbd_cbd_dataset=SO_before[np.logical_and(    np.logical_and(np.squeeze(treatment_cbd)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

SO_before_combined_no_rgs=np.concatenate([SO_before_veh_cbd_dataset,SO_before_cbd_cbd_dataset,SO_before_veh_osbasic_dataset]);


hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = stats.zscore(SO_before_veh_osbasic_dataset), title='Veh OS Basic',clipmin=-1,clipmax=1)
#hplt.plot_umap(x=u_veh_rgs[:,0],y=u_veh_rgs[:,1],feature = SO_before_veh_rgs_dataset, title='Veh treatment- RGS dataset',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = stats.zscore(SO_before_veh_cbd_dataset), title='Veh treatment- CBD dataset',clipmin=-1,clipmax=1)
#hplt.plot_umap(x=u_rgs_rgs[:,0],y=u_rgs_rgs[:,1],feature = SO_before_rgs_rgs_dataset, title='RGS treatment- RGS dataset',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = stats.zscore(SO_before_cbd_cbd_dataset),title='CBD treatment- CBD dataset',clipmin=-1,clipmax=1)
#hplt.plot_umap(x=u_clean[:,0],y=u_clean[:,1],feature = SO_before_combined,title='Combined',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = stats.zscore(SO_before_combined_no_rgs),title='Combined (No RGS)',clipmin=-1,clipmax=1)
# %%
from scipy import stats
#SO_afterz=stats.zscore(SO_after)

SO_after_veh_osbasic_dataset=SO_after[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_osbasic)==1)]
SO_after_veh_rgs_dataset=SO_after[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
SO_after_veh_cbd_dataset=SO_after[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

#Non-Controls:
SO_after_rgs_rgs_dataset=SO_after[np.logical_and(    np.logical_and(np.squeeze(treatment_rgs)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
SO_after_cbd_cbd_dataset=SO_after[np.logical_and(    np.logical_and(np.squeeze(treatment_cbd)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

SO_after_combined_no_rgs=np.concatenate([SO_after_veh_cbd_dataset,SO_after_cbd_cbd_dataset,SO_after_veh_osbasic_dataset]);


hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = stats.zscore(SO_after_veh_osbasic_dataset), title='Veh OS Basic',clipmin=-1,clipmax=1)
#hplt.plot_umap(x=u_veh_rgs[:,0],y=u_veh_rgs[:,1],feature = SO_after_veh_rgs_dataset, title='Veh treatment- RGS dataset',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = stats.zscore(SO_after_veh_cbd_dataset), title='Veh treatment- CBD dataset',clipmin=-1,clipmax=1)
#hplt.plot_umap(x=u_rgs_rgs[:,0],y=u_rgs_rgs[:,1],feature = SO_after_rgs_rgs_dataset, title='RGS treatment- RGS dataset',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = stats.zscore(SO_after_cbd_cbd_dataset),title='CBD treatment- CBD dataset',clipmin=-1,clipmax=1)
#hplt.plot_umap(x=u_clean[:,0],y=u_clean[:,1],feature = SO_after_combined,title='Combined',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = stats.zscore(SO_after_combined_no_rgs),title='Combined (No RGS)',clipmin=-1,clipmax=1)

# %%
S_entropy_veh_osbasic_dataset=S_entropy[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_osbasic)==1)]
S_entropy_veh_rgs_dataset=S_entropy[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
S_entropy_veh_cbd_dataset=S_entropy[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

#Non-Controls:
S_entropy_rgs_rgs_dataset=S_entropy[np.logical_and(    np.logical_and(np.squeeze(treatment_rgs)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
S_entropy_cbd_cbd_dataset=S_entropy[np.logical_and(    np.logical_and(np.squeeze(treatment_cbd)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

S_entropy_combined_no_rgs=np.concatenate([S_entropy_veh_cbd_dataset,S_entropy_cbd_cbd_dataset,S_entropy_veh_osbasic_dataset]);


hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = S_entropy_veh_osbasic_dataset, title='Veh OS Basic',clipmin=2,clipmax=4.5)
#hplt.plot_umap(x=u_veh_rgs[:,0],y=u_veh_rgs[:,1],feature = S_entropy_veh_rgs_dataset, title='Veh treatment- RGS dataset',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = S_entropy_veh_cbd_dataset, title='Veh treatment- CBD dataset',clipmin=2,clipmax=4.5)
#hplt.plot_umap(x=u_rgs_rgs[:,0],y=u_rgs_rgs[:,1],feature = S_entropy_rgs_rgs_dataset, title='RGS treatment- RGS dataset',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = S_entropy_cbd_cbd_dataset,title='CBD treatment- CBD dataset',clipmin=2,clipmax=4.5)
#hplt.plot_umap(x=u_clean[:,0],y=u_clean[:,1],feature = S_entropy_combined,title='Combined',clipmin=0,clipmax=130)
hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = S_entropy_combined_no_rgs,title='Combined (No RGS)',clipmin=2,clipmax=4.5)


# %% Splitting days.

#Controls
StudyDay_rip_osbasic=StudyDay_rip[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_osbasic)==1)]
# L=np.logical_and(    np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_osbasic)==1) , np.squeeze(StudyDay_rip)=='OR'  );
# v1_cond=hplt.get_kde_contours(x=u_veh_osbasic[L,0], y=u_veh_osbasic[L,1])
StudyDay_rip_veh_rgs=StudyDay_rip[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
StudyDay_rip_veh_cbd=StudyDay_rip[np.logical_and(    np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]

#Non-Controls:
StudyDay_rip_rgs_rgs=StudyDay_rip[np.logical_and(    np.logical_and(np.squeeze(treatment_rgs)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_rgs)==1)]
StudyDay_rip_cbd_cbd=StudyDay_rip[np.logical_and(    np.logical_and(np.squeeze(treatment_cbd)==1,np.logical_not(outliers_combined))  ,  np.squeeze(dataset_cbd)==1)]


#Data_combined_no_rgs=np.concatenate([Data_veh_cbd_dataset,Data_cbd_cbd_dataset,Data_veh_osbasic_dataset]);

StudyDay_rip_combined_no_rgs=np.concatenate([StudyDay_rip_veh_cbd,StudyDay_rip_cbd_cbd,StudyDay_rip_osbasic])
StudyDay_rip_combined=StudyDay_rip[np.logical_not(outliers_combined)];



def get_kde_contour(x, y, level_index=7,levels=10 ):
    kde=kdeplot(x,y)
    p = kde.collections[level_index].get_paths()[0]
    v = p.vertices
    return v


#OS basic
L=np.squeeze(StudyDay_rip_osbasic=='OD');
v_osbasic_OD=get_kde_contour(x=u_veh_osbasic[L,0], y=u_veh_osbasic[L,1])
close()
L=np.squeeze(StudyDay_rip_osbasic=='OR');
v_osbasic_OR=get_kde_contour(x=u_veh_osbasic[L,0], y=u_veh_osbasic[L,1])
close()
L=np.squeeze(StudyDay_rip_osbasic=='CN');
v_osbasic_CN=get_kde_contour(x=u_veh_osbasic[L,0], y=u_veh_osbasic[L,1])
close()
L=np.squeeze(StudyDay_rip_osbasic=='HC');
v_osbasic_HC=get_kde_contour(x=u_veh_osbasic[L,0], y=u_veh_osbasic[L,1])
close()


def plot_conditions(embedding,studyday_embedding,no_cn=0):
    L=np.squeeze(studyday_embedding=='OD');
    v_OD=get_kde_contour(x=embedding[L,0], y=embedding[L,1])
    close()
    L=np.squeeze(studyday_embedding=='OR');
    v_OR=get_kde_contour(x=embedding[L,0], y=embedding[L,1])
    close()
    if no_cn==0:    
        L=np.squeeze(studyday_embedding=='CN');
        v_CN=get_kde_contour(x=embedding[L,0], y=embedding[L,1])
        close()
    
    L=np.squeeze(studyday_embedding=='HC');
    v_HC=get_kde_contour(x=embedding[L,0], y=embedding[L,1])
    close()    
    if no_cn==0:    
        return (v_OD,v_OR,v_CN,v_HC)
    else:
        return (v_OD,v_OR,v_HC)
        
# %%

# OS BASIC
fig, ax = plt.subplots()
#hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = Amp_veh_osbasic_dataset, title='Veh OS Basic',clipmin=0,clipmax=4.5)
hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = Meanfreq_veh_osbasic_dataset, title='Veh OS Basic',clipmin=100,clipmax=200)
#hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = Duration_veh_osbasic_dataset, title='Veh OS Basic',clipmin=0,clipmax=100)
#hplt.plot_umap(x=u_veh_osbasic[:,0],y=u_veh_osbasic[:,1],feature = S_entropy_veh_osbasic_dataset, title='Veh OS Basic',clipmin=2,clipmax=4.5)


plt.plot(v_osbasic_OD[:,0],v_osbasic_OD[:,1],'yellow')
plt.scatter(np.mean(v_osbasic_OD[:,0]),np.mean(v_osbasic_OD[:,1]),c='yellow',s=200, marker='+')
plt.plot(v_osbasic_OR[:,0],v_osbasic_OR[:,1],'teal')
plt.scatter(np.mean(v_osbasic_OR[:,0]),np.mean(v_osbasic_OR[:,1]),c='teal',s=200, marker='+')
plt.plot(v_osbasic_CN[:,0],v_osbasic_CN[:,1],'blueviolet')
plt.scatter(np.mean(v_osbasic_CN[:,0]),np.mean(v_osbasic_CN[:,1]),c='blueviolet',s=200, marker='+')
plt.plot(v_osbasic_HC[:,0],v_osbasic_HC[:,1],'black')
plt.scatter(np.mean(v_osbasic_HC[:,0]),np.mean(v_osbasic_HC[:,1]),c='black',s=200, marker='+')

ax.legend(['Stable', 'Overlapping','Random control', 'Homecage'])
plt.xlim([-1,11])
plt.ylim([-1,11])

centroids_os_basic=[ (np.mean(v_osbasic_OD[:,0]),np.mean(v_osbasic_OD[:,1])) ,
(np.mean(v_osbasic_OR[:,0]),np.mean(v_osbasic_OR[:,1])) ,
(np.mean(v_osbasic_CN[:,0]),np.mean(v_osbasic_CN[:,1])) ,
(np.mean(v_osbasic_HC[:,0]),np.mean(v_osbasic_HC[:,1])),
]
#OD, OR, CN ,HC

# %%

# #VEH RGS
# [v_veh_rgs_OD,v_veh_rgs_OR,v_veh_rgs_CN,v_veh_rgs_HC]=plot_conditions(u_veh_rgs,StudyDay_rip_veh_rgs)
# fig, ax = plt.subplots()
# hplt.plot_umap(x=u_veh_rgs[:,0],y=u_veh_rgs[:,1],feature = Meanfreq_veh_rgs_dataset, title='Veh RGS',clipmin=100,clipmax=200)
# plt.plot(v_veh_rgs_OD[:,0],v_veh_rgs_OD[:,1],'yellow')
# plt.plot(v_veh_rgs_OR[:,0],v_veh_rgs_OR[:,1],'teal')
# plt.plot(v_veh_rgs_CN[:,0],v_veh_rgs_CN[:,1],'blueviolet')
# plt.plot(v_veh_rgs_HC[:,0],v_veh_rgs_HC[:,1],'black')
# ax.legend(['Stable', 'Overlapping','Random control', 'Homecage'])
# plt.xlim([-1,11])
# plt.ylim([-1,11])


#VEH CBD
[v_veh_cbd_OD,v_veh_cbd_OR,v_veh_cbd_HC]=plot_conditions(u_veh_cbd,StudyDay_rip_veh_cbd,no_cn=1)

fig, ax = plt.subplots()
# hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = Meanfreq_veh_cbd_dataset, title='Veh CBD',clipmin=100,clipmax=200)
#hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = Amp_veh_cbd_dataset, title='Veh CBD',clipmin=0,clipmax=4.5)
#hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = Duration_veh_cbd_dataset, title='Veh CBD',clipmin=0,clipmax=100)
hplt.plot_umap(x=u_veh_cbd[:,0],y=u_veh_cbd[:,1],feature = S_entropy_veh_cbd_dataset, title='Veh CBD',clipmin=2,clipmax=4.5)

plt.plot(v_veh_cbd_OD[:,0],v_veh_cbd_OD[:,1],'yellow')
plt.scatter(np.mean(v_veh_cbd_OD[:,0]),np.mean(v_veh_cbd_OD[:,1]),c='yellow',s=200, marker='+')
plt.plot(v_veh_cbd_OR[:,0],v_veh_cbd_OR[:,1],'teal')
plt.scatter(np.mean(v_veh_cbd_OR[:,0]),np.mean(v_veh_cbd_OR[:,1]),c='teal',s=200, marker='+')

#plt.plot(v_veh_cbd_CN[:,0],v_veh_cbd_CN[:,1],'blueviolet')
plt.plot(v_veh_cbd_HC[:,0],v_veh_cbd_HC[:,1],'black')
plt.scatter(np.mean(v_veh_cbd_HC[:,0]),np.mean(v_veh_cbd_HC[:,1]),c='black',s=200, marker='+')

ax.legend(['Stable', 'Overlapping', 'Homecage'])
plt.xlim([-1,11])
plt.ylim([-1,11])


centroids_veh_cbd=[ (np.mean(v_veh_cbd_OD[:,0]),np.mean(v_veh_cbd_OD[:,1])) ,
(np.mean(v_veh_cbd_OR[:,0]),np.mean(v_veh_cbd_OR[:,1])) ,
(np.mean(v_veh_cbd_HC[:,0]),np.mean(v_veh_cbd_HC[:,1])),
]
#OD, OR,HC

# # RGS RGS
# [v_rgs_rgs_OD,v_rgs_rgs_OR,v_rgs_rgs_CN,v_rgs_rgs_HC]=plot_conditions(u_rgs_rgs,StudyDay_rip_rgs_rgs,no_cn=0)
# fig, ax = plt.subplots()
# hplt.plot_umap(x=u_rgs_rgs[:,0],y=u_rgs_rgs[:,1],feature = Meanfreq_rgs_rgs_dataset, title='RGS RGS',clipmin=100,clipmax=200)
# plt.plot(v_rgs_rgs_OD[:,0],v_rgs_rgs_OD[:,1],'yellow')
# plt.plot(v_rgs_rgs_OR[:,0],v_rgs_rgs_OR[:,1],'teal')
# plt.plot(v_rgs_rgs_CN[:,0],v_rgs_rgs_CN[:,1],'blueviolet')
# plt.plot(v_rgs_rgs_HC[:,0],v_rgs_rgs_HC[:,1],'black')
# ax.legend(['Stable', 'Overlapping','Random control', 'Homecage'])
# plt.xlim([-1,11])
# plt.ylim([-1,11])

# %%
#CBD CBD
[v_cbd_cbd_OD,v_cbd_cbd_OR,v_cbd_cbd_HC]=plot_conditions(u_cbd_cbd,StudyDay_rip_cbd_cbd,no_cn=1)

fig, ax = plt.subplots()
#hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = Meanfreq_cbd_cbd_dataset, title='CBD CBD',clipmin=100,clipmax=200)
# hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = Amp_cbd_cbd_dataset, title='CBD CBD',clipmin=0,clipmax=4.5)
#hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = Duration_cbd_cbd_dataset, title='CBD CBD',clipmin=0,clipmax=100)
hplt.plot_umap(x=u_cbd_cbd[:,0],y=u_cbd_cbd[:,1],feature = S_entropy_cbd_cbd_dataset, title='CBD CBD',clipmin=2,clipmax=4.5)


plt.plot(v_cbd_cbd_OD[:,0],v_cbd_cbd_OD[:,1],'yellow')
plt.scatter(np.mean(v_cbd_cbd_OD[:,0]),np.mean(v_cbd_cbd_OD[:,1]),c='yellow',s=200, marker='+')

plt.plot(v_cbd_cbd_OR[:,0],v_cbd_cbd_OR[:,1],'teal')
plt.scatter(np.mean(v_cbd_cbd_OR[:,0]),np.mean(v_cbd_cbd_OR[:,1]),c='teal',s=200, marker='+')

#plt.plot(v_veh_cbd_CN[:,0],v_veh_cbd_CN[:,1],'blueviolet')
plt.plot(v_cbd_cbd_HC[:,0],v_cbd_cbd_HC[:,1],'black')
plt.scatter(np.mean(v_cbd_cbd_HC[:,0]),np.mean(v_cbd_cbd_HC[:,1]),c='black',s=200, marker='+')

ax.legend(['Stable', 'Overlapping', 'Homecage'])
plt.xlim([-1,11])
plt.ylim([-1,11])

centroids_cbd_cbd=[ (np.mean(v_cbd_cbd_OD[:,0]),np.mean(v_cbd_cbd_OD[:,1])) ,
(np.mean(v_cbd_cbd_OR[:,0]),np.mean(v_cbd_cbd_OR[:,1])) ,
(np.mean(v_cbd_cbd_HC[:,0]),np.mean(v_cbd_cbd_HC[:,1])),
]

#OD, OR,HC

# %%


#u_combined_no_rgs
[v_combined_no_rgs_OD,v_combined_no_rgs_OR,v_combined_no_rgs_CN,v_combined_no_rgs_HC]=plot_conditions(u_combined_no_rgs,StudyDay_rip_combined_no_rgs,no_cn=0)

fig, ax = plt.subplots()
#hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = Meanfreq_combined_no_rgs, title='Combined (no-RGS)',clipmin=100,clipmax=200)
#hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = Amp_combined_no_rgs, title='Combined (no-RGS)',clipmin=0,clipmax=4.5)
#hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = Duration_combined_no_rgs, title='Combined (no-RGS)',clipmin=0,clipmax=100)
hplt.plot_umap(x=u_combined_no_rgs[:,0],y=u_combined_no_rgs[:,1],feature = S_entropy_combined_no_rgs, title='Combined (no-RGS)',clipmin=2,clipmax=4.5)


plt.plot(v_combined_no_rgs_OD[:,0],v_combined_no_rgs_OD[:,1],'yellow')
plt.scatter(np.mean(v_combined_no_rgs_OD[:,0]),np.mean(v_combined_no_rgs_OD[:,1]),c='yellow',s=200, marker='+')


plt.plot(v_combined_no_rgs_OR[:,0],v_combined_no_rgs_OR[:,1],'teal')
plt.scatter(np.mean(v_combined_no_rgs_OR[:,0]),np.mean(v_combined_no_rgs_OR[:,1]),c='teal',s=200, marker='+')

plt.plot(v_combined_no_rgs_CN[:,0],v_combined_no_rgs_CN[:,1],'blueviolet')
plt.scatter(np.mean(v_combined_no_rgs_CN[:,0]),np.mean(v_combined_no_rgs_CN[:,1]),c='blueviolet',s=200, marker='+')

plt.plot(v_combined_no_rgs_HC[:,0],v_combined_no_rgs_HC[:,1],'black')
plt.scatter(np.mean(v_combined_no_rgs_HC[:,0]),np.mean(v_combined_no_rgs_HC[:,1]),c='black',s=200, marker='+')

ax.legend(['Stable', 'Overlapping','Random control', 'Homecage'])
plt.xlim([-1,11])
plt.ylim([-1,11])


centroids_combined_no_rgs=[ (np.mean(v_combined_no_rgs_OD[:,0]),np.mean(v_combined_no_rgs_OD[:,1])) ,
(np.mean(v_combined_no_rgs_OR[:,0]),np.mean(v_combined_no_rgs_OR[:,1])) ,
(np.mean(v_combined_no_rgs_CN[:,0]),np.mean(v_combined_no_rgs_CN[:,1])) ,
(np.mean(v_combined_no_rgs_HC[:,0]),np.mean(v_combined_no_rgs_HC[:,1])),
]
#OD, OR, CN ,HC


with open('centroids_cbd_cbd.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(centroids_cbd_cbd, f)
with open('centroids_os_basic.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(centroids_os_basic, f)
with open('centroids_veh_cbd.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(centroids_veh_cbd, f)
with open('centroids_combined_no_rgs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(centroids_combined_no_rgs, f)

import pickle
with open('centroids_os_basic.pkl','rb') as f: )
    centroids_os_basic= pickle.load(f)    

# %%

# #u combined.
# [v_combined_OD,v_combined_OR,v_combined_CN,v_combined_HC]=plot_conditions(u_clean,StudyDay_rip_combined,no_cn=0)
# fig, ax = plt.subplots()
# hplt.plot_umap(x=u_clean[:,0],y=u_clean[:,1],feature = Meanfreq_combined, title='Combined',clipmin=100,clipmax=200)
# plt.plot(v_combined_OD[:,0],v_combined_OD[:,1],'yellow')
# plt.plot(v_combined_OR[:,0],v_combined_OR[:,1],'teal')
# plt.plot(v_combined_CN[:,0],v_combined_CN[:,1],'blueviolet')
# plt.plot(v_combined_HC[:,0],v_combined_HC[:,1],'black')
# ax.legend(['Stable', 'Overlapping','Random control', 'Homecage'])
# plt.xlim([-1,11])
# plt.ylim([-1,11])

# ax.legend(['Stable', 'Overlapping','Random control', 'Homecage'])


# %%


# CODE ENDS HERE.


# Controls
#u_veh_osbasic = fit.fit_transform(Data_veh_osbasic_dataset)
u_veh_rgs = fit.fit_transform(Data_veh_rgs_dataset)
u_veh_cbd = fit.fit_transform(Data_veh_cbd_dataset)
# Non-controls
u_rgs_rgs = fit.fit_transform(Data_rgs_rgs_dataset)
u_cbd_cbd = fit.fit_transform(Data_cbd_cbd_dataset)

    

# %% Find HC ripples to establish baseline
#StudyDay
# StudyDay_rip
# #Trial
# trial_rip

#SD_hc=hproc.strcmp(StudyDay_rip,"HC") #OSBASIC #RGS14
L_veh=np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers)[0]);
SD_veh=StudyDay_rip[L_veh];
trial_veh=trial_rip[L_veh];



L=np.squeeze(SD_veh=='OD');
string='OD VEH'
hplt.plot_density(u_veh_treatment[L,0],u_veh_treatment[L,1],title=string+" ripples",figsize =(10, 7),vmax=0.25)

L=np.squeeze(SD_veh=='OR');
string='OR VEH'
L=np.squeeze(StudyDay_rip_osbasic=='OD');
v_osbasic_OD=get_kde_contour(x=u_veh_osbasic[L,0], y=u_veh_osbasic[L,1])
close()
L=np.squeeze(StudyDay_rip_osbasic=='OR');
v_osbasic_OD=get_kde_contour(x=u_veh_osbasic[L,0], y=u_veh_osbasic[L,1])
close()
L=np.squeeze(StudyDay_rip_osbasic=='CN');
v_osbasic_CN=get_kde_contour(x=u_veh_osbasic[L,0], y=u_veh_osbasic[L,1])
close()
L=np.squeeze(StudyDay_rip_osbasic=='HC');
v_osbasic_HC=get_kde_contour(x=u_veh_osbasic[L,0], y=u_veh_osbasic[L,1])
close()
hplt.plot_density(u_veh_treatment[L,0],u_veh_treatment[L,1],title=string+" ripples",figsize =(10, 7),vmax=0.25)

L=np.squeeze(SD_veh=='CN');
string='CN VEH'
hplt.plot_density(u_veh_treatment[L,0],u_veh_treatment[L,1],title=string+" ripples",figsize =(10, 7),vmax=0.25)

L=np.squeeze(SD_veh=='HC');
string='HC VEH'
hplt.plot_density(u_veh_treatment[L,0],u_veh_treatment[L,1],title=string+" ripples",figsize =(10, 7),vmax=0.25)




L=np.squeeze(SD_veh=='OD');
v1_cond=get_kde_contour(x=u_veh_treatment[L,0], y=u_veh_treatment[L,1])
close()

L=np.squeeze(SD_veh=='OR');
v2_cond=get_kde_contour(x=u_veh_treatment[L,0], y=u_veh_treatment[L,1],level_index=6)
close()
L=np.squeeze(SD_veh=='CN');
v3_cond=get_kde_contour(x=u_veh_treatment[L,0], y=u_veh_treatment[L,1])
close()
L=np.squeeze(SD_veh=='HC');
v4_cond=get_kde_contour(x=u_veh_treatment[L,0], y=u_veh_treatment[L,1])
close()


fig, ax = plt.subplots()
plt.plot(v1_cond[:,0],v1_cond[:,1],'orange')
plt.plot(v2_cond[:,0],v2_cond[:,1],'teal')
plt.plot(v3_cond[:,0],v3_cond[:,1],'blueviolet')
plt.plot(v4_cond[:,0],v4_cond[:,1],'black')
ax.legend(['Stable', 'Overlapping','Random control', 'Homecage'])


# %% Trial data for HC.


L=np.squeeze(SD_veh=='HC');
string='HC VEH'
hplt.plot_density(u_veh_treatment[L,0],u_veh_treatment[L,1],title=string+" ripples",figsize =(10, 7),vmax=0.25)
cm = plt.get_cmap('gist_rainbow')
NUM_COLORS=8;


L=np.logical_and(np.squeeze(SD_veh=='HC'),np.squeeze(trial_veh=='Post1'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*0/NUM_COLORS))
c_hc_pt1=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='HC'),np.squeeze(trial_veh=='Post2'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*1/NUM_COLORS))
c_hc_pt2=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='HC'),np.squeeze(trial_veh=='Post3'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*2/NUM_COLORS))
c_hc_pt3=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]

L=np.logical_and(np.squeeze(SD_veh=='HC'),np.squeeze(trial_veh=='Post4'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*3/NUM_COLORS))
c_hc_pt4=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='HC'),np.squeeze(trial_veh=='Post5-1'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*4/NUM_COLORS))
c_hc_pt5_1=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='HC'),np.squeeze(trial_veh=='Post5-2'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*5/NUM_COLORS))
c_hc_pt5_2=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='HC'),np.squeeze(trial_veh=='Post5-3'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*6/NUM_COLORS))
c_hc_pt5_3=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='HC'),np.squeeze(trial_veh=='Post5-4'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*7/NUM_COLORS))
c_hc_pt5_4=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]

# %% Overlapping

L=np.squeeze(SD_veh=='OR');
string='OR VEH'
hplt.plot_density(u_veh_treatment[L,0],u_veh_treatment[L,1],title=string+" ripples",figsize =(10, 7),vmax=0.25)
cm = plt.get_cmap('gist_rainbow')
NUM_COLORS=8;


L=np.logical_and(np.squeeze(SD_veh=='OR'),np.squeeze(trial_veh=='Post1'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*0/NUM_COLORS))
c_or_pt1=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='OR'),np.squeeze(trial_veh=='Post2'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*1/NUM_COLORS))
c_or_pt2=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='OR'),np.squeeze(trial_veh=='Post3'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*2/NUM_COLORS))
c_or_pt3=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]

L=np.logical_and(np.squeeze(SD_veh=='OR'),np.squeeze(trial_veh=='Post4'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*3/NUM_COLORS))
c_or_pt4=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]

L=np.logical_and(np.squeeze(SD_veh=='OR'),np.squeeze(trial_veh=='Post5-1'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*4/NUM_COLORS))
c_or_pt5_1=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='OR'),np.squeeze(trial_veh=='Post5-2'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*5/NUM_COLORS))
c_or_pt5_2=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='OR'),np.squeeze(trial_veh=='Post5-3'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*6/NUM_COLORS))
c_or_pt5_3=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


L=np.logical_and(np.squeeze(SD_veh=='OR'),np.squeeze(trial_veh=='Post5-4'))
plt.plot(np.nanmean(u_veh_treatment[L,0]),np.nanmean(u_veh_treatment[L,1]),'o',color=cm(1.*7/NUM_COLORS))
c_or_pt5_4=[np.nanmean(u_veh_treatment[L,0]), np.nanmean(u_veh_treatment[L,1])]


# %% COMBINED embedding
#u_clean=fit.fit_transform(Data[np.logical_not(outliers)[0]])

treatment_comb=np.squeeze(treatment_rip[np.logical_not(outliers)[0]])
L_comb_veh=treatment_comb=='CBD';
string='Veh'
hplt.plot_density(u_clean[L_comb_veh,0],u_clean[L_comb_veh,1],title=string+" ripples",figsize =(10, 7),vmax=0.25)


L_comb_veh=treatment_comb=='CBD';
v1=get_kde_contour(x=u_clean[L_comb_veh,0], y=u_clean[L_comb_veh,1])
close()
L_comb_veh=treatment_comb=='RGS';
v2=get_kde_contour(x=u_clean[L_comb_veh,0], y=u_clean[L_comb_veh,1],level_index=6)
close()
L_comb_veh=treatment_comb=='VEH';
v3=get_kde_contour(x=u_clean[L_comb_veh,0], y=u_clean[L_comb_veh,1])
close()




ax = fig.add_subplot()
L_comb_veh=treatment_comb=='CBD';
plt.plot(u_clean[L_comb_veh,0], u_clean[L_comb_veh,1], 'k.', markersize=2)  
plt.plot(v1[:,0],v1[:,1],'lime')

plt.plot(v5[:,0],v5[:,1],'blue')
plt.plot(v3[:,0],v3[:,1],'red')
plt.xlabel( 'Umap 1')
plt.ylabel( 'Umap 2')
plt.title('Combined embedding')
#L_hc=np.logical_and(L_veh,np.squeeze(SD_hc)==1)

#hplt.plot_density(u[L,0],u[L,1],title=string+" ripples",figsize =(10, 7),vmax=0.25)


#Data_veh_treatment=Data[np.logical_and(np.squeeze(treatment_veh)==1,np.logical_not(outliers)[0])]



#hplt.plot_density(u[L,0],u[L,1],title=string+" ripples",figsize =(10, 7),vmax=0.25)



# %%
#Dataset
dataset_np=T[:,0]

#Treatment
treatment_np=T[:,1]

#Rat
rat_np=T[:,2]
#StudyDay
StudyDay_np=T[:,3]
#Trial
trial_np=T[:,4]



dataset=hproc.strcmp(dataset_np,"CBDchronic") #OSBASIC #RGS14
dataset1=hproc.strcmp(dataset_np,"RGS14") #OSBASIC #RGS14
dataset2=hproc.strcmp(dataset_np,"OSBASIC") #OSBASIC #RGS14


#dataset=dataset+dataset1+dataset2; #All datasets


#Treatment
treatment=hproc.strcmp(treatment_np, "VEH")

#Rat
#rat=hproc.strcmp(rat_np, "Rat1")

#StudyDay
studyday=hproc.strcmp(StudyDay_np, "HC")

#Trial
trial=hproc.strcmp(trial_np, "Post5-4")
trial_p=hproc.strcmp(trial_np, "Post5-3");
trial=np.logical_or(trial,trial_p)

L_dataset=hproc.binary_feature(Ripples,dataset)
L_treatment=hproc.binary_feature(Ripples,treatment)
L_studyday=hproc.binary_feature(Ripples,studyday)
L_trial=hproc.binary_feature(Ripples, trial)

var_bin=np.logical_and(L_dataset,L_treatment);
var_bin=np.logical_and(var_bin,L_studyday);

var_bin_pre=np.logical_and(var_bin,L_trial)

var_bin=np.logical_and(np.logical_not(all_outliers), var_bin); #Not outlier and complies to conditions. 

x=Data[var_bin,:];
x_ps=Data[var_bin_pre,:];
# %% 
#[k1,k2]=isomapDimEst(x);
# %% Fit UMAP for all treatements

x=Data;
fit = umap.UMAP(n_components=4)
u=fit.fit_transform(x);

hplt.plot3Ddensity(u[:,0],u[:,1],u[:,2],zlabel='umap3',bins=50)
# %%

u_hc_osbasic = fit.fit_transform(x)

hplt.plot3Ddensity(u_hc_osbasic[:,0],u_hc_osbasic[:,1],u_hc_osbasic[:,2], zlabel='umap 3', bins=50)


kmeans = KMeans(n_clusters=7, random_state=0).fit(x)
label = kmeans.labels_

p3d =plt.scatter(u_hc_osbasic[:,1],u_hc_osbasic[:,3],c=label, s=1)
plt.colorbar(p3d)

#plt.plot(np.mean(x[label==0,:],0))

# %% 

fit = umap.UMAP(n_components=4)
u_hc_osbasic_ps = fit.fit_transform(x_ps)
hplt.plot3Ddensity(u_hc_osbasic_ps[:,0],u_hc_osbasic_ps[:,1],u_hc_osbasic_ps[:,2], zlabel='umap 3', bins=50)

plt.scatter(u_hc_osbasic_ps[:,0],u_hc_osbasic_ps[:,1])
# %% Compute DimEst for umap using isomap. 
# K1=[];
# for i in range(100):
#     n=np.random.choice(Data.shape[0], 20000)
#     data=Data[n,:];
#     k1,k2=isomapDimEst(data)
#     K1.append(k1);

# K2=K1;
# %% Ripples data
#[k1,k2]=isomapDimEst(x);
# %%

# %%



#Dataset
dataset_np=T[:,0]

#Treatment
treatment_np=T[:,1]

#Rat
rat_np=T[:,2]
#StudyDay
StudyDay_np=T[:,3]
#Trial
trial_np=T[:,4]

#Ripples waveforms
Ripples=T[:,5]


### -

### Global variables



# myDict2 = scipy.io.loadmat('Tcell_ripples.mat')
# T_ripples=myDict2['Tcell_ripples'];




#Amplitude
amplitude_np=T[:,5]

#Meanfreq
meanfreq_np=T[:,6]


#Amplitude2
amplitude2_np=T[:,7]


#Frequency
freq_np=T[:,8]

#Entropy
entropy_np=T[:,9]

#AUC
auc_np=T[:,10]

#AUC2
auc2_np=T[:,11]

#Duration
# dur_np=T_ripples[:,5];


Data = hproc.v_stack(Ripples)


# %% Compute DimEst for umap using isomap. 
# K1=[];
# for i in range(100):
#     n=np.random.choice(Data.shape[0], 20000)
#     data=Data[n,:];
#     k1,k2=isomapDimEst(data)
#     K1.append(k1);

# K2=K1;
# [k1,k2]=isomapDimEst(Data);


# fit = umap.UMAP(n_components=4)
# u = fit.fit_transform(Data)
  
# %% 3D density plot

condition = ["CON", "OD", "OR", "HC"]
# scipy.io.savemat(f'{ROOT_DIR}/u.mat',{'umap1':u[:,0], 'umap2':u[:,1], 'umap3':u[:,2], 'umap4':u[:,3],})

# TODO: Uncomment this
# for con in ["CON"]:                                             # supply condition to loop over all conditions
#     for i in range(8,9):                                        # use range(10) to loop over all rats
#         rat=hproc.strcmp(rat_np, f"Rat{i}")
#         studyday=hproc.strcmp(StudyDay_np, con)
#         res = rat*studyday
#         L=hproc.binary_feature(Ripples,res)
#         hplt.plot3Ddensity(u[L,0],u[L,1],u[L,3],s=30)

# %%
#Features per ripple    
Amp=hproc.h_stack(amplitude_np)
Meanfreq=hproc.h_stack(meanfreq_np)
Amp2=hproc.h_stack(amplitude2_np)
Freq=hproc.h_stack(freq_np)
Entropy=hproc.h_stack(entropy_np)
AUC=hproc.h_stack(auc_np)
AUC2=hproc.h_stack(auc2_np)


#DUR=get_duration(dur_np);
# TODO: Uncomment this
# hplt.plot_umap(u[:,0],u[:,1],feature= Amp,clipmin= 10,title="Amplitude1 (z-scored)",s=1)
# hplt.plot_umap(u[:,0],u[:,1],feature= Freq,clipmax=120,title="Frequency",s=1)
# hplt.plot_umap(u[:,0],u[:,1],feature= Entropy,title="Entropy",s=1)
# hplt.plot_umap(u[:,0],u[:,1],feature= AUC,title="Area under the curve",s=1)
# hplt.plot_umap(u[:,0],u[:,1],feature= AUC2,title="Area under the curve 2",s=1)


#plot_umap(DUR,"Duration (ms)")
# %% Look for features ranges and their overlap.


t_freq=hplt.plot_umap(u[:,0],u[:,1],feature= Freq,title="Frequency",s=1)
t_amp=hplt.plot_umap(u[:,0],u[:,1],feature= Amp,title="Amplitude",s=1)
t_ent=hplt.plot_umap(u[:,0],u[:,1],feature= Entropy,title="Entropy",s=1)


t_freq=hplt.plot_umap(u[:,0],u[:,1],feature= Freq,clipmin=160,title="Frequency",s=1)
t_amp=hplt.plot_umap(u[:,0],u[:,1],feature= Amp,clipmax=2,title="Amplitude",s=1)
t_ent=hplt.plot_umap(u[:,0],u[:,1],feature= Entropy,clipmin=3.75,title="Entropy",s=1)


x=np.logical_and(t_freq,t_amp);
x1=np.logical_and(x,t_ent);

hplt.plot_umap_binary(u[x1,0],u[x1,1] ,title="Overlap",s=1)

# %% Baseline ripples

dataset=hproc.strcmp(dataset_np,"OSBASIC") #OSBASIC #RGS14

#Treatment
treatment=hproc.strcmp(treatment_np, "VEH")

#Rat
#rat=hproc.strcmp(rat_np, "Rat1")

#StudyDay
studyday=hproc.strcmp(StudyDay_np, "HC")

#Trials    
#trial=hproc.strcmp(trial_np,"Post1")

L_dataset=hproc.binary_feature(Ripples,dataset)
L_treatment=hproc.binary_feature(Ripples,treatment)
L_studyday=hproc.binary_feature(Ripples,studyday)

var_bin=np.logical_and(L_dataset,L_treatment);
var_bin=np.logical_and(var_bin,L_studyday);
#var_bin=np.logical_and(L_dataset,L_treatment);


Data_osbasic_hc = hproc.v_stack(Ripples)
fit = umap.UMAP(n_components=4)

#u_hc = fit.fit_transform(Data_osbasic_hc(L,:))



# %% RGS ripples
string="VEH"
treatment=hproc.strcmp(treatment_np, string)
L=hproc.binary_feature(Ripples,treatment)


L=hproc.binary_feature(Ripples,dataset)

#plot_umap_binary(L,"RGS14")
# TODO: Uncomment this
# hplt.plot_density(u[L,0],u[L,1],title=string+" ripples",figsize =(10, 7),vmax=0.25)



# %% Rat's ripples
rat=hproc.strcmp(rat_np, "Rat9")
L=hproc.binary_feature(Ripples,rat)

# TODO: Uncomment this
# hplt.plot_density(u[L,0], u[L,1],title="Ripples from Rat 9",figsize =(10, 7),vmax=0.25)
# %% OS
string="VEH"
studyday=hproc.strcmp(StudyDay_np, "OR")
st2=hproc.strcmp(StudyDay_np, "OD")
st3=hproc.strcmp(StudyDay_np, "CON")
treatment=hproc.strcmp(treatment_np, string)
logicresult=studyday*treatment;
logicresult2=st2*treatment;
logicresult3=st3*treatment;

x=np.logical_or(logicresult,logicresult2)
x1=np.logical_or(x,logicresult3)


L=hproc.binary_feature(Ripples,x1)
# TODO: Uncomment this
# hplt.plot_density(u[L,0],u[L,1],title="Ripples from " +string+ " OS",figsize =(10, 7),vmax=0.25)

#OR
L=hproc.binary_feature(Ripples,studyday)
# TODO: Uncomment this
# hplt.plot_density(u[L,0],u[L,1],title="Ripples from " +string+ " OR",figsize =(10, 7),vmax=0.25)

string="VEH"
studydayhc=hproc.strcmp(StudyDay_np, "HC")
treatment=hproc.strcmp(treatment_np, string)
vehhpc=studydayhc*treatment

#HC
L=hproc.binary_feature(Ripples,vehhpc)
# TODO: Uncomment this
# hplt.plot_density(u[L,0],u[L,1],title="Ripples from " +string+ " HC",figsize =(10, 7),vmax=0.25)



# %% Homecage
string="RGS14"

studyday=hproc.strcmp(StudyDay_np, "HC")
treatment=hproc.strcmp(treatment_np, string)
logicresult=studyday*treatment

L=hproc.binary_feature(Ripples,logicresult)
# TODO: Uncomment this
# hplt.plot_density(u[L,0],u[L,1],title="Ripples from "+string+" HC",figsize =(10, 7),vmax=0.25)


# %% Significant clusters 

# features = [Meanfreq, Amp, Amp2, Freq, Entropy, AUC, AUC2]
# labels = ['Mean Frequency', 'Amp', 'Amp2', 'Frequency', 'Entropy', 'AUC', 'AUC2']

features = [Meanfreq]
labels = ['Mean Frequency']
x = u[:,0] # between -10 and 4, log-gamma of an svc
y = u[:,1]
# TODO: Uncomment this
print(x.shape[0],len(features[0][:-2].shape) != 0,features[0][:-2][0].shape)
img, sig_ind = hplt.significant_pixels(x,y,features,iter=1000,featureLabel=labels ,s=25,pval=0.05)
# sig_ind = np.array(sig_ind)
# np.save('sig_ind.npy',sig_ind)
# hplt.plotZfeatureOnDensities(x,y,features, featureLabel=labels)
sig_ind = np.load('sig_ind.npy')

