import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io
import umap
import URC_computeClusterIndex_V4
import os
import time
#import sys
os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');

st = time.time()

myDict = scipy.io.loadmat('Tcell.mat')
T=myDict['Tcell'];

Ripples=T[:,4];
auc_np=T[:,10];

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

fit = umap.UMAP(n_components=4)
u = fit.fit_transform(Data)
df=pd.DataFrame(u, columns=['u1','u2','u3','u4'])
auc=flatcells(auc_np);
      
#cI_val, bLab, _=URC_computeClusterIndex_V4.computeClusterIndex_V4(df,Meanfreq,10,['u1','u2'],plotCluster=0,vmin=100, vmax=250)
z=auc;
vmin=np.mean(z)-3*np.std(z);
vmax=np.mean(z)+3*np.std(z);

cI_val_array=[]
for i in range(4):
    for k in range(4):
        if i==k:
            cI_val=0
        else:
            cI_val, bLab, _=URC_computeClusterIndex_V4.computeClusterIndex_V4(df,auc,10,[df.columns[i],df.columns[k]],plotCluster=0,vmin=vmin, vmax=vmax)
        cI_val_array.append(cI_val)


fig,ax = plt.subplots()
cI_val_array=np.array(cI_val_array)
cI_val_array.resize(4,4)
im1 = plt.imshow(cI_val_array, cmap=plt.cm.Greys)


plt.xticks([0,1,2,3], [1,2,3,4])
plt.yticks([0,1,2,3], [1,2,3,4])



plt.xlabel('UMAP', loc='center')
plt.ylabel('UMAP', loc='center')
plt.title("Structure Index \n (AUC)")

plt.colorbar()

plt.show()


et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')





