#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:54:42 2022

@author: adrian
"""

import os

os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');

import scipy.io
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

import umap

sns.set(style='white',context='poster', rc={'figure.figsize':(14,10)} )

# %%
myDict = scipy.io.loadmat('AMP.mat')

AmpDF=pd.DataFrame.from_dict(myDict['Amp']);

A=AmpDF[0]; 


# %%
myDict = scipy.io.loadmat('Ripples.mat')

#trial1=myDict['Ripples'][0];

#RipplesDF=pd.DataFrame.from_dict(myDict['Ripples'][0]) ##m is between 0 and (length(ripples)-1) (0-287)
RipplesDF=pd.DataFrame.from_dict(myDict['Ripples']) ##m is between 0 and (length(ripples)-1) (0-287)


a=RipplesDF[0]; #ripplesDF[0][0][x][y] => x and y is row and column numbers, indexing starts with 0.

#data=a;

# %%
## Random data
np.random.seed(42)
data = np.random.rand(800, 4)


fit = umap.UMAP()
u = fit.fit_transform(data)


plt.scatter(u[:,0],u[:,1],c=data)
plt.title('UMAP embedding of random colours');


# %% Ripples data
b=a[0];
fit = umap.UMAP(n_components=4)
u = fit.fit_transform(b)


colours=np.random.rand(b.shape[0], 1)
plt.scatter(u[:,0],u[:,1],c=colours)
plt.title('UMAP embedding of ripples');

# %%
a_np=RipplesDF.to_numpy();
amp_np=A.to_numpy();
#v1=a_np[0][0];
#v2=a_np[1][0];
#v3=a_np[2][0];
#v4=np.vstack((v1,v3));


v1=amp_np[0][0];
v2=amp_np[1];
v3=amp_np[2][0];


v4=np.append(v1,v3)

Data=[];
for i in range(len(a_np)):
    print(i)
#    Data=np.vstack((Data,x[i][0]));
    if i==0:
        Data=a_np[i][0];
        continue
    try:
        Data=np.vstack((Data,a_np[i][0]));
    except ValueError:
        print('Empty cell')
        continue



    
#Amplitude    
Amp=[];
for i in range(len(a_np)):
    print(i)
#    Data=np.vstack((Data,x[i][0]));
    if i==0:
        Amp=amp_np[i][0];
        continue
    try:
     Amp=np.hstack((Amp,amp_np[i][0]));
    except IndexError:
        print('Empty cell')
        continue
 

       
 
 
 #v4=np.vstack((v1,v3));       
        
        
        
        
  #  except ValueError:
  #      print('Empty cell')
  #      continue
  #  except IndexError:
  #      print('Empty cell')
  #      continue
        


fit = umap.UMAP(n_components=4)
u = fit.fit_transform(Data)
# %%


#colours=np.random.rand(u.shape[0], 1)

#z=Amp;
#colors = plt.cm.viridis(z)

#plt.title('UMAP embedding of ripples');
#plt.clim(np.min(scipy.stats.zscore(Amp)), np.max(scipy.stats.zscore(Amp)))


z=scipy.stats.zscore(Amp);

colormap=plt.cm.get_cmap('bwr')
colors=colormap(z)
sm=plt.scatter(u[:,0],u[:,1],c=colors)
sm=plt.cm.ScalarMappable(cmap=colormap)
sm.set_clim(vmin=np.min(z),vmax=np.max(z))
plt.colorbar(sm)
plt.xlabel("UMAP1")
plt.ylabel("UMAP2")
plt.title("UMAP embedding of ripple z-scored amplitudes")
plt.show()




