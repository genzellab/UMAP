#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:54:42 2022

@author: adrian
"""

import os
import sys
os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');
#sys.path.append('/home/genzel/Documents/UMAP')

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
# Data will be a matrix X by 127, where X is the pooled amount of ripples across all trials. 

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
# %% Compute DimEst for umap using isomap. 
# K1=[];
# for i in range(100):
#     n=np.random.choice(Data.shape[0], 20000)
#     data=Data[n,:];
#     k1,k2=isomapDimEst(data)
#     K1.append(k1);

# K2=K1;
# %% Ripples data
# [k1,k2]=isomapDimEst(Data);


# fit = umap.UMAP(n_components=4)
# u = fit.fit_transform(Data)
u=np.load('u.npy');

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


def plot_umap_3D(Amp,string):
    z=Amp;
    normalize = cl.Normalize(vmin=np.mean(z)-3*np.std(z), vmax=np.mean(z)+3*np.std(z))
    
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')

    sm=ax.scatter(list(u[:,0]), list(u[:,1]), list(u[:,3]),c=z,alpha=0.6,s=1,cmap='seismic',norm=normalize)
    
    plt.colorbar(sm)
    ax.set_xlabel('UMAP1')
    ax.set_ylabel('UMAP2')
    ax.set_zlabel('UMAP4')
    plt.title(string)

    plt.show()



# def plot_umap_binary(L,string):
#     #z=Amp;
#     #normalize = cl.Normalize(vmin=np.mean(z)-3*np.std(z), vmax=np.mean(z)+3*np.std(z))
    
#     #colormap=plt.cm.get_cmap('bwr')
#     #colors=colormap(z)
#     #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.01)g
#     #sm=plt.scatter(u[:,0],u[:,1],alpha=0.1,s=5,color="b")
#     plt.scatter(u[L,0],u[L,1],alpha=0.1,s=20,color="r")   
#     #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.1,cmap='seismic')
#     #plt.hist2d(u[L,0], u[L,1],100)
#     #sm=plt.cm.ScalarMappable(cmap=colormap)
    
#     #sm.set_clim(vmin=np.min(z),vmax=np.max(z))
#     #sm.set_clim(vmin=np.min(z),vmax=220)
    
#     #plt.colorbar(sm)
#     plt.xlabel("UMAP1")
#     plt.ylabel("UMAP2")
#     plt.title(string)
#     plt.show()
#     #plt.legend(['First line', 'Second line'])

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

def plot3Ddensity(x,y,z, bins = 100):
    X = np.linspace(x.min(), x.max(), num=bins+1)
    Y = np.linspace(y.min(), y.max(), num=bins+1)
    Z = np.linspace(z.min(), z.max(), num=bins+1)
    data = []
    for xi in range(1,bins+1):
        for yi in range(1,bins+1):
            for zi in range(1,bins+1):
                tx = np.logical_and(x < X[xi], x >= X[xi-1])
                ty = np.logical_and(y < Y[yi], y >= Y[yi-1])
                tz = np.logical_and(z < Z[zi], z >= Z[zi-1])
                assert(tx.shape == ty.shape)
                assert(ty.shape == tz.shape)
                t = np.logical_and(tx,ty)
                t = np.logical_and(t,tz)
                data.append([X[xi-1], Y[yi-1], Z[zi-1], x[t].sum() + y[t].sum() + z[t].sum()] )
    data = np.array(data)
    datap = data[:,3]>0.0
    print(data.shape, datap.shape)
    data = data[datap]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    print(type(data[:,3]),data[0,3])
    p3d = ax.scatter(data[:,0], data[:,1], data[:,2], s=30, c=data[:,3].tolist(),linewidths=0.5)
    ax.set_xlabel('umap1')
    ax.set_ylabel('umap2')
    ax.set_zlabel('umap4')
    plt.show()
    
# %%    
def significant_pixels(ratString, dayString,binning,p_val):
# Determines which pixels have a significant density compared to
# a permuted control.
#PARAMETERS:
#ratString
#dayString
#binning: Suggested: 100. It gives a 100x100 density matrix. 
#p_val: P-value. Suggested: 0.001    
    
    #ratString='Rat1'
    #dayString='CON'
    
    #Rat
    rat=strcmp(rat_np, ratString)
    

    #Trial
    trial =  strcmp(StudyDay_np, dayString)
    

    logicresult=trial*rat;

    L=binary_feature(Ripples,logicresult)
    
    t_unshuffled=(u[L, :2]);
    
    a=plt.hist2d(u[L,0], u[L,1],binning,density=1);
    a0=a[0];
    a1=a[1];
    a2=a[2];
    #a3=a[3];
    #B=np.zeros([100,100]);
    B=[];
    for i in range(1000):    
        L_permuted=np.random.permutation(L);  # This line
        b=plt.hist2d(u[L_permuted,0], u[L_permuted,1],binning,density=1);
        b0=b[0];
        b0=np.ndarray.flatten(b0)
        #B = array([B,b0])
        #B.append(b0);
        if i==0:
            B=b0;
        else:
            B=np.vstack((B,b0))
    a0=np.ndarray.flatten(a0)     

    #p-value calculation (Plusmaze method)   
    D0=[]
    for i in range(a0.size):
        #max(B[:,i])
        distribution=B[:,i];
        #m_d=np.mean(distribution)
        d0=(1+np.sum(distribution >=a0[i]))/(len(distribution)+1) ;
        if i==0:
            D0=d0;
        else:
            D0=np.vstack((D0,d0))
               
    D=D0<=p_val;         
            
                         
    D1=np.reshape(D,(binning,binning))     
    return D1
    
    
# %% 3D density plot

condition = ["CON", "OD", "OR", "HC"]
# scipy.io.savemat(f'{ROOT_DIR}/u.mat',{'umap1':u[:,0], 'umap2':u[:,1], 'umap3':u[:,2], 'umap4':u[:,3],})
for con in ["CON"]:
    for i in range(8,9):
        rat=strcmp(rat_np, f"Rat{i}")
        studyday=strcmp(StudyDay_np, con)
        res = rat*studyday
        L=binary_feature(Ripples,res)
        plot3Ddensity(u[L,0],u[L,1],u[L,3])

# %%
#Features per ripple    
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


#OR
L=binary_feature(Ripples,studyday)
plot_binary(L,"Ripples from " +string+ " OR")


string="VEH"
studydayhc=strcmp(StudyDay_np, "HC")
treatment=strcmp(treatment_np, string)
vehhpc=studydayhc*treatment

#HC
L=binary_feature(Ripples,vehhpc)
plot_binary(L,"Ripples from " +string+ " HC")



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


