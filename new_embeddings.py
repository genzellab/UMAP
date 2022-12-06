#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 13:05:45 2022

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

Ripples_cbd=T_cbd[:,5]
Ripples_cbd=Ripples_cbd[2:];
Data_cbd = hproc.v_stack(Ripples_cbd)

Ripples_rgs=T_rgs[:,5]
Data_rgs = hproc.v_stack(Ripples_rgs)

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
hplt.plot_umap_binary(u_rgs[:,0],u_rgs[:,2] ,title="RGS14",s=1,xlabel='Umap 1',ylabel='Umap 3',c='#0343DF')
plt.xlim([-1,11])
plt.ylim([-1,11])

hplt.plot_umap_binary(u_osbasic[:,1],u_osbasic[:,2] ,title="OS basic",s=1,xlabel='UMAP2',ylabel='UMAP3',c='#E50000')
plt.xlim([-1,11])
plt.ylim([-1,11])

hplt.plot_umap_binary(u_cbd[:,1],u_cbd[:,3] ,title="CBD",s=1,xlabel='Umap 2', ylabel='Umap 4', c='#15B01A')
plt.xlim([-1,11])
plt.ylim([-1,11])

hplt.plot_umap_binary(u[:,1],u[:,3] ,title="Combined",s=1,xlabel='Umap 2', ylabel='Umap 4')
plt.xlim([-1,11])
plt.ylim([-1,11])

# %%
#Density
hplt.plot3Ddensity(u_rgs[:,0],u_rgs[:,1],u_rgs[:,2], zlabel='umap 3', bins=50)

hplt.plot3Ddensity(u_cbd[:,0],u_cbd[:,1],u_cbd[:,3], zlabel='umap 4', bins=50)

hplt.plot3Ddensity(u_osbasic[:,0],u_osbasic[:,1],u_osbasic[:,2], zlabel='umap 3', bins=50)


hplt.plot3Ddensity(u[:,0],u[:,1],u[:,3], zlabel='umap 4', bins=50)

# %% Remove outliers using K-means clustering.

#OS BASIC
a=u_osbasic[:,0:2];

# kmeans = KMeans(n_clusters=4, random_state=0).fit(a)
# label = kmeans.labels_

clustering = DBSCAN(eps=0.2, min_samples=10).fit(a)
label=clustering.labels_


fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot()
p3d =plt.scatter(u_osbasic[:,0],u_osbasic[:,1],c=label, s=10,cmap='viridis')
plt.colorbar(p3d)
ax.set_xlabel('Umap 1')
ax.set_ylabel('Umap 2')
plt.title('OS basic')

outliers_osbasic=[label==1];
# %%
#RGS14
a=u_rgs[:,0:2];

clustering = DBSCAN(eps=0.2, min_samples=10).fit(a)
label=clustering.labels_


fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot()
p3d =plt.scatter(u_rgs[:,0],u_rgs[:,1],c=label, s=10,cmap='viridis')
plt.colorbar(p3d)
ax.set_xlabel('Umap 1')
ax.set_ylabel('Umap 2')
plt.title('RGS14')

outliers_rgs=[label==1];

# %% 
# CBD

a=u_cbd[:,0:2];

clustering = DBSCAN(eps=0.2, min_samples=5).fit(a)
label=clustering.labels_


fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot()
p3d =plt.scatter(u_cbd[:,0],u_cbd[:,1],c=label, s=10,cmap='viridis')
plt.colorbar(p3d)
ax.set_xlabel('Umap 1')
ax.set_ylabel('Umap 2')
plt.title('CBD')

outliers_cbd=[label==1];
# %%
# Combined
a=u[:,0:2];

clustering = DBSCAN(eps=0.2, min_samples=5).fit(a)
label=clustering.labels_


fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot()
p3d =plt.scatter(u[:,0],u[:,1],c=label, s=10,cmap='viridis')
plt.colorbar(p3d)
ax.set_xlabel('Umap 1')
ax.set_ylabel('Umap 2')
plt.title('Combined')

outliers=[label==1];

# %% Re compute UMAP without outliers

fit = umap.UMAP(n_components=4)
u_clean=fit.fit_transform(Data[np.logical_not(outliers)[0]])
u_cbd_clean = fit.fit_transform(Data_cbd[np.logical_not(outliers_cbd)[0]])
u_rgs_clean = fit.fit_transform(Data_rgs[np.logical_not(outliers_rgs)[0]])
u_osbasic_clean = fit.fit_transform(Data_osbasic[np.logical_not(outliers_osbasic)[0]])


# %% Figures, describing embeddings.
# def cm2inch(value):
#     return value/2.54
# figsize=(cm2inch(3.5), cm2inch(3.5))
# plt.figure(figsize=(cm2inch(12.8), cm2inch(9.6)))

#2D
#plt.rc('axes', labelsize=40)
hplt.plot_umap_binary(u_rgs_clean[:,0],u_rgs_clean[:,1] ,title="RGS14",s=1,xlabel='Umap 1',ylabel='Umap 2',c='#0343DF')
plt.xlim([-1,11])
plt.ylim([-1,11])

hplt.plot_umap_binary(u_osbasic_clean[:,0],u_osbasic_clean[:,1] ,title="OS basic",s=1,xlabel='Umap 1',ylabel='Umap 2',c='#E50000')
plt.xlim([-1,11])
plt.ylim([-1,11])

hplt.plot_umap_binary(u_cbd_clean[:,0],u_cbd_clean[:,1] ,title="CBD",s=1,xlabel='Umap 1', ylabel='Umap 2', c='#15B01A')
plt.xlim([-1,11])
plt.ylim([-1,11])

hplt.plot_umap_binary(u_clean[:,0],u_clean[:,1] ,title="Combined",s=1,xlabel='Umap 1', ylabel='Umap 2')
plt.xlim([-1,11])
plt.ylim([-1,11])
