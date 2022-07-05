#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:54:42 2022

@author: adrian
"""

import os
import sys
os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');

import scipy.io
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cl

from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

import umap
#import plotly.express as px
from URC_computeIsomapDimEst import isomapDimEst

sns.set(style='white',context='poster', rc={'figure.figsize':(14,10)} )
# %% Load whole table and split columns 

myDict = scipy.io.loadmat('Tcell.mat')
T=myDict['Tcell'];


# myDict2 = scipy.io.loadmat('Tcell_ripples.mat')
# T_ripples=myDict2['Tcell_ripples'];


#Treatment
treatment_np=T[:,0];
#Rat
rat_np=T[:,1];
#StudyDay
StudyDay_np=T[:,2];
#Trial
trial_np=T[:,3];

#Amplitude
amplitude_np=T[:,5];

#Ripples waveforms
Ripples=T[:,4];

#Meanfreq
meanfreq_np=T[:,6];


#Amplitude2
amplitude2_np=T[:,7];


#Frequency
freq_np=T[:,8];

#Entropy
entropy_np=T[:,9];

#AUC
auc_np=T[:,10];

#AUC2
auc2_np=T[:,11];

#Duration
# dur_np=T_ripples[:,5];

# %% Flattening

Data=[];
for i in range(len(Ripples)):
    print(i)
#    Data=np.vstack((Data,x[i][0]));
    if i==0:
        Data=Ripples[i];
        continue
    try:
        Data=np.vstack((Data,Ripples[i]));
    except ValueError:
        print('Empty cell')
        continue


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

# K1=[];
# for i in range(100):
#     n=np.random.choice(Data.shape[0], 20000)
#     data=Data[n,:];
#     k1,k2=isomapDimEst(data)
#     K1.append(k1);

# K2=K1;
# %% Ripples data
[k1,k2]=isomapDimEst(Data);


fit = umap.UMAP(n_components=4)
u = fit.fit_transform(Data)

# %% Functions
def get_duration(dur_np):
    DUR=[]
    for i in range(len(dur_np)):
        print(i);
    #    Data=np.vstack((Data,x[i][0]));
        if i==0:
            DUR=dur_np[i];
            continue
        try:
         DUR=np.vstack((DUR,dur_np[i]));
        except ValueError:
            print('Empty cell')
            continue
    return DUR


#Function to accumulate values from numpy arrays
def flatcells(amplitude_np):    
    Amp=[];
    for i in range(len(amplitude_np)):
        print(i);
    #    Data=np.vstack((Data,x[i][0]));
        if i==0:
            Amp=amplitude_np[i][0];
            continue
        try:
         Amp=np.hstack((Amp,amplitude_np[i][0]));
        except IndexError:
            print('Empty cell')
            continue
    return Amp


#Function to compare strings with numpy arrays.
def strcmp(treatment_np,string):
    Amp=[];
    for i in range(len(treatment_np)):
        print(i);
    #    Data=np.vstack((Data,x[i][0]));
        if treatment_np[i][0]==string:
            Amp.append(1)
        else:
            Amp.append(0)
    A=np.array(Amp)       
    return A
 
def plot_umap(Amp,string):
    z=Amp;
    normalize = cl.Normalize(vmin=np.mean(z)-3*np.std(z), vmax=np.mean(z)+3*np.std(z))
    
    #colormap=plt.cm.get_cmap('bwr')
    #colors=colormap(z)
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.01)g
    sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=1,cmap='seismic',norm=normalize)
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.1,cmap='seismic')
    
    #sm=plt.cm.ScalarMappable(cmap=colormap)
    
    #sm.set_clim(vmin=np.min(z),vmax=np.max(z))
    #sm.set_clim(vmin=np.min(z),vmax=220)
    
    plt.colorbar(sm)
    plt.xlabel("UMAP1")
    plt.ylabel("UMAP2")
    plt.title(string)
    plt.show()


def plot_umap_binary(L,string):
    #z=Amp;
    #normalize = cl.Normalize(vmin=np.mean(z)-3*np.std(z), vmax=np.mean(z)+3*np.std(z))
    
    #colormap=plt.cm.get_cmap('bwr')
    #colors=colormap(z)
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.01)g
    #sm=plt.scatter(u[:,0],u[:,1],alpha=0.1,s=5,color="b")
    plt.scatter(u[L,0],u[L,1],alpha=0.1,s=20,color="r")   
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.1,cmap='seismic')
    #plt.hist2d(u[L,0], u[L,1],100)
    #sm=plt.cm.ScalarMappable(cmap=colormap)
    
    #sm.set_clim(vmin=np.min(z),vmax=np.max(z))
    #sm.set_clim(vmin=np.min(z),vmax=220)
    
    #plt.colorbar(sm)
    plt.xlabel("UMAP1")
    plt.ylabel("UMAP2")
    plt.title(string)
    plt.show()
    #plt.legend(['First line', 'Second line'])

def plot_binary(L,string):
    #z=Amp;
    #normalize = cl.Normalize(vmin=np.mean(z)-3*np.std(z), vmax=np.mean(z)+3*np.std(z))
    
    #colormap=plt.cm.get_cmap('bwr')
    #colors=colormap(z)
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.01)g
    #sm=plt.scatter(u[:,0],u[:,1],alpha=0.1,s=5,color="b")
    #plt.scatter(u[L,0],u[L,1],alpha=0.1,s=20,color="r")   
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.1,cmap='seismic')
    fig, ax = plt.subplots(figsize =(10, 7))
    plt.hist2d(u[L,0], u[L,1],100,density=1)
    cmb=plt.colorbar()
    cmb.mappable.set_clim(vmin=0, vmax=0.25)    
    cmb.set_label('Density')
    #sm=plt.cm.ScalarMappable(cmap=colormap)
    sm=plt.cm.ScalarMappable()

    #sm.set_clim(vmin=np.min(z),vmax=np.max(z))
    sm.set_clim(vmin=0,vmax=0.2)
    ax.set_xlabel('UMAP1') 
    ax.set_ylabel('UMAP2') 
    #plt.colorbar(sm)
    #plt.xlabel("UMAP1")
    #plt.ylabel("UMAP2")
    plt.title(string)
  
    # show plot
    plt.tight_layout() 
    plt.show()
    
   
    

def binary_feature(Ripples,treatment):   
    L=[]
    for i in range(len(Ripples)):
        v=Ripples[i];
        l=v.shape[0];
        if l==0:
            continue
        else:
            L.extend([treatment[i]]*l)
    L=np.array(L);
    L=L==1;
    return L
# %%
#Features    
Amp=flatcells(amplitude_np);
Meanfreq=flatcells(meanfreq_np);

Amp2=flatcells(amplitude2_np);
Freq=flatcells(freq_np);
Entropy=flatcells(entropy_np);
AUC=flatcells(auc_np);

AUC2=flatcells(auc2_np);

#DUR=get_duration(dur_np);


plot_umap(Amp,"Amplitude1 (z-scored)")
plot_umap(Freq,"Frequency")

plot_umap(Entropy,"Entropy")

plot_umap(AUC,"Area under the curve")

plot_umap(AUC2,"Area under the curve 2")

#plot_umap(DUR,"Duration (ms)")

# %%
#Treatment
treatment=strcmp(treatment_np, "RGS14")

#Rat
rat=strcmp(rat_np, "Rat1")

#StudyDay
studyday=strcmp(StudyDay_np, "OR")

#Trials    
trial=strcmp(trial_np,"Post1")


# %% RGS ripples
string="VEH"
treatment=strcmp(treatment_np, string)
L=binary_feature(Ripples,treatment)
#plot_umap_binary(L,"RGS14")
plot_binary(L,string+" ripples")

# %% Rat's ripples
rat=strcmp(rat_np, "Rat9")
L=binary_feature(Ripples,rat)
plot_binary(L,"Ripples from Rat 9")
# %% OS
string="VEH"
studyday=strcmp(StudyDay_np, "OR")
st2=strcmp(StudyDay_np, "OD")
st3=strcmp(StudyDay_np, "CON")
treatment=strcmp(treatment_np, string)
logicresult=studyday*treatment;
logicresult2=st2*treatment;
logicresult3=st3*treatment;

x=np.logical_or(logicresult,logicresult2)
x1=np.logical_or(x,logicresult3)


L=binary_feature(Ripples,x1)
plot_binary(L,"Ripples from " +string+ " OS")


# %% Homecage
string="RGS14"

studyday=strcmp(StudyDay_np, "HC")
treatment=strcmp(treatment_np, string)
logicresult=studyday*treatment;

L=binary_feature(Ripples,logicresult)
plot_binary(L,"Ripples from "+string+" HC")


# %%



#z=scipy.stats.zscore(Meanfreq);
#z=(Amp);

# %%


