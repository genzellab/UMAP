#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:54:42 2022

@author: adrian
"""

import os
import sys
# TODO: Select path wrt your system
# os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');
os.chdir('/home/blazkowiz47/work/UMAP/dataset');
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

sns.set(style='white',context='poster', rc={'figure.figsize':(14,10)} )
# %% Load whole table and split columns 
### Start Loading data

myDict = scipy.io.loadmat('Tcell.mat')
u=np.load('u.npy')

### -

### Global variables

T=myDict['Tcell']


# myDict2 = scipy.io.loadmat('Tcell_ripples.mat')
# T_ripples=myDict2['Tcell_ripples'];


#Treatment
treatment_np=T[:,0]
#Rat
rat_np=T[:,1]
#StudyDay
StudyDay_np=T[:,2]
#Trial
trial_np=T[:,3]

#Amplitude
amplitude_np=T[:,5]

#Ripples waveforms
Ripples=T[:,4]

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

### -

# c=[];
# for i in range(len(Ripples)):
#     print(i)
#     if i==0:
#         c=dur_np[i];
#         continue
#     try:
#         c=np.vstack((c,dur_np[i]))
#     except ValueError:
#         print('Empty cell')
#         continue
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

# %%

#Treatment
treatment=hproc.strcmp(treatment_np, "RGS14")

#Rat
rat=hproc.strcmp(rat_np, "Rat1")

#StudyDay
studyday=hproc.strcmp(StudyDay_np, "OR")

#Trials    
trial=hproc.strcmp(trial_np,"Post1")


# %% RGS ripples
string="VEH"
treatment=hproc.strcmp(treatment_np, string)
L=hproc.binary_feature(Ripples,treatment)
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

features = [Meanfreq, Amp, Amp2, Freq, Entropy, AUC, AUC2]
labels = ['Mean Frequency', 'Amp', 'Amp2', 'Frequency', 'Entropy', 'AUC', 'AUC2']

# features = [Meanfreq]
# labels = ['Mean Frequency']
x = u[:,0] # between -10 and 4, log-gamma of an svc
y = u[:,1]
# TODO: Uncomment this
print(x.shape[0],len(features[0][:-2].shape) != 0,features[0][:-2][0].shape)
img, sig_ind = hplt.significant_pixels(x,y,features,iter=1000,featureLabel=labels ,s=25,pval=0.05)
# sig_ind = np.array(sig_ind)
# np.save('sig_ind.npy',sig_ind)
# hplt.plotZfeatureOnDensities(x,y,features, featureLabel=labels)
sig_ind = np.load('sig_ind.npy')

