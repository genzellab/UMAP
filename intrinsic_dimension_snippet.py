#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 13:57:05 2023

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
from URC_computeIsomapDimEst import isomapDimEst
import utils.plotting_helpers as hplt
import utils.processing_helpers as hproc
from sklearn.cluster import KMeans, DBSCAN
from seaborn import kdeplot
import pickle
from multiprocessing import Pool




# # Load UMAP embeddings:
with open('embeddings.pkl','rb') as f:  # Python 3: open(..., 'rb')
    embeddings= pickle.load(f)    

u_veh_osbasic=embeddings[0];
u_veh_rgs=embeddings[1];
u_veh_cbd=embeddings[2];
u_cbd_cbd=embeddings[3];
u_rgs_rgs=embeddings[4];
u_clean=embeddings[5];  #Combines all
u_combined_no_rgs=embeddings[6];


## Load ripples (free of outliers)
with open('Data.pkl','rb') as f:  # Python 3: open(..., 'rb')
    Data= pickle.load(f)    

Data_veh_osbasic_dataset=Data[0];
Data_veh_rgs_dataset=Data[1];
Data_veh_cbd_dataset=Data[2];
Data_cbd_cbd_dataset=Data[3];
Data_rgs_rgs_dataset=Data[4];
Data_clean=Data[5]; #Combines all
Data_combined_no_rgs=Data[6];


#%% Determine intrinsic dimensionality

#Select data to work with
Data=Data_veh_osbasic_dataset;

# This one usually gives memory issues.
[k1,k2]=isomapDimEst(Data);

# Uncomment for a bootstrapping method that uses less memory. 

#for x in range(100):
#     n=np.random.choice(Data.shape[0], 20000)
#     data=Data[n,:];
#     [k1,k2]=isomapDimEst(data);
#     K1.append(k1);

def bootstrapped_isomap(data):
    [k1,k2]=isomapDimEst(data)
    return k1
def data_gen(n):
    for _ in range(n):
        x=np.random.choice(Data.shape[0], 1000)
        yield Data[x,:];
with Pool() as p:
    K1 = p.map(bootstrapped_isomap, data_gen(100))
print(np.mean(K1))

