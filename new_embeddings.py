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

myDict = scipy.io.loadmat('Tcell_03_12_2022.mat')
T=myDict['Tcell']

myDict = scipy.io.loadmat('Tcell_cbd_03_12_2022.mat')
T_cbd=myDict['cbd']

myDict = scipy.io.loadmat('Tcell_RGS14_03_12_2022.mat')
T_rgs=myDict['rgs14']

myDict = scipy.io.loadmat('Tcell_OSBASIC_03_12_2022.mat')
T_osbasic=myDict['osbasic']


#Ripples waveforms
Ripples=T[:,5]
Data = hproc.v_stack(Ripples[2:])
#Dataset
dataset_np=T[:,0]
dataset_rip=hproc.unfold_days2ripples(Ripples,dataset_np)
#Treatment
treatment_np=T[:,1]
treatment_rip=hproc.unfold_days2ripples(Ripples,treatment_np)
#Rat
rat_np=T[:,2]
rat_rip=hproc.unfold_days2ripples(Ripples, rat_np)
#StudyDay
StudyDay_np=T[:,3]
StudyDay_rip=hproc.unfold_days2ripples(Ripples, StudyDay_np)
#Trial
trial_np=T[:,4]
trial_rip=hproc.unfold_days2ripples(Ripples,trial_np)


Ripples_cbd=T_cbd[:,5]
Ripples_cbd=Ripples_cbd[2:];
Data_cbd = hproc.v_stack(Ripples_cbd)

Ripples_rgs=T_rgs[:,5]
Data_rgs = hproc.v_stack(Ripples_rgs)
treatment_np_rgs=T_rgs[:,1]
treatment_rip_rgs=hproc.unfold_days2ripples(Ripples_rgs,treatment_np_rgs)


Ripples_osbasic=T_osbasic[:,5]
Data_osbasic = hproc.v_stack(Ripples_osbasic)

# %%  Compute UMAP
fit = umap.UMAP(n_components=4)
u=fit.fit_transform(Data)
u_cbd = fit.fit_transform(Data_cbd)
u_rgs = fit.fit_transform(Data_rgs)
u_osbasic = fit.fit_transform(Data_osbasic)

# %% Figures, describing embeddings.
# def cm2inch(value):
#     return value/2.54
# figsize=(cm2inch(3.5), cm2inch(3.5))
# plt.figure(figsize=(cm2inch(12.8), cm2inch(9.6)))


#2D
hplt.plot_umap_binary(u_rgs[:,0],u_rgs[:,2] ,title="RGS14 dataset",s=1,xlabel='Umap 1',ylabel='Umap 3',c='#0343DF')
plt.xlim([-1,11])
plt.ylim([-1,11])

hplt.plot_umap_binary(u_osbasic[:,1],u_osbasic[:,2] ,title="OS basic dataset",s=1,xlabel='UMAP2',ylabel='UMAP3',c='#E50000')
plt.xlim([-1,11])
plt.ylim([-1,11])

hplt.plot_umap_binary(u_cbd[:,1],u_cbd[:,3] ,title="CBD dataset",s=1,xlabel='Umap 2', ylabel='Umap 4', c='#15B01A')
plt.xlim([-1,11])
plt.ylim([-1,11])

hplt.plot_umap_binary(u[:,1],u[:,3] ,title="Combined datasets",s=1,xlabel='Umap 2', ylabel='Umap 4')
plt.xlim([-1,11])
plt.ylim([-1,11])

# %%
#Density
hplt.plot3Ddensity(u_rgs[:,0],u_rgs[:,1],u_rgs[:,2], zlabel='umap 3', bins=50)

hplt.plot3Ddensity(u_cbd[:,0],u_cbd[:,1],u_cbd[:,3], zlabel='umap 4', bins=50)

hplt.plot3Ddensity(u_osbasic[:,0],u_osbasic[:,1],u_osbasic[:,2], zlabel='umap 3', bins=50)


hplt.plot3Ddensity(u[:,0],u[:,1],u[:,3], zlabel='umap 4', bins=50)

# %% Remove outliers using DBSCAN clustering.


[outliers_osbasic]=hplt.dbscan_outliers(u_osbasic, "OS_basic", eps_value=0.2, min_samples_value=10)
[outliers_rgs]=hplt.dbscan_outliers(u_rgs, "RGS14", eps_value=0.2, min_samples_value=10)
[outliers_cbd]=hplt.dbscan_outliers(u_cbd, "CBD", eps_value=0.10, min_samples_value=1)
[outliers]=hplt.dbscan_outliers(u, "Combined", eps_value=0.2, min_samples_value=5)


# %% Using combined outliers from all datasets. 
outliers_combined=np.concatenate([outliers_cbd,outliers_osbasic,outliers_rgs]);


# %% Re compute UMAP without outliers

fit = umap.UMAP(n_components=4)
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
    hplt.plot_umap_binary(item[:,0],item[:,1] ,title=names,s=1,xlabel='Umap 1',ylabel='Umap 2',c=colours)
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
#Dataset
dataset_rip
#Treatment
treatment_rip
#Rat
rat_rip
#StudyDay
StudyDay_rip
#Trial
trial_rip

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
    hplt.plot_umap_binary(item[:,0],item[:,1] ,title=names,s=1,xlabel='Umap 1',ylabel='Umap 2',c=colours)
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
    hplt.plot_umap_binary(item[:,0],item[:,1] ,title=names,s=1,xlabel='Umap 1',ylabel='Umap 2',c=colours)
    plt.xlim([-1,11])
    plt.ylim([-1,11])



