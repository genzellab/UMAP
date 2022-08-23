import os
import sys
os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');

from scipy import ndimage
from scipy.ndimage import center_of_mass
from numpy import array, stack
import scipy.io
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cl

from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

import umap

sns.set(style='white',context='poster', rc={'figure.figsize':(14,10)} )
# %% Load whole table and split columns 

myDict = scipy.io.loadmat('Tcell.mat')
T=myDict['Tcell'];


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



#Trials   
trial_hc=strcmp(trial_np,"Presleep") & strcmp(StudyDay_np, "HC")
trial_or=strcmp(trial_np,"Presleep") & strcmp(StudyDay_np, "OR")
trial_od=strcmp(trial_np,"Presleep") & strcmp(StudyDay_np, "OD")
trial_con=strcmp(trial_np,"Presleep") & strcmp(StudyDay_np, "CON")
 
trial1_hc=strcmp(trial_np,"Post1") & strcmp(StudyDay_np, "HC")
trial1_or=strcmp(trial_np,"Post1") & strcmp(StudyDay_np, "OR")
trial1_od=strcmp(trial_np,"Post1") & strcmp(StudyDay_np, "OD")
trial1_con=strcmp(trial_np,"Post1") & strcmp(StudyDay_np, "CON")

trial2_hc=strcmp(trial_np,"Post2") & strcmp(StudyDay_np, "HC")
trial2_or=strcmp(trial_np,"Post2") & strcmp(StudyDay_np, "OR")
trial2_od=strcmp(trial_np,"Post2") & strcmp(StudyDay_np, "OD")
trial2_con=strcmp(trial_np,"Post2") & strcmp(StudyDay_np, "CON")

trial3_hc=strcmp(trial_np,"Post3") & strcmp(StudyDay_np, "HC")
trial3_or=strcmp(trial_np,"Post3") & strcmp(StudyDay_np, "OR")
trial3_od=strcmp(trial_np,"Post3") & strcmp(StudyDay_np, "OD")
trial3_con=strcmp(trial_np,"Post3") & strcmp(StudyDay_np, "CON")

trial4_hc=strcmp(trial_np,"Post4") & strcmp(StudyDay_np, "HC")
trial4_or=strcmp(trial_np,"Post4") & strcmp(StudyDay_np, "OR")
trial4_od=strcmp(trial_np,"Post4") & strcmp(StudyDay_np, "OD")
trial4_con=strcmp(trial_np,"Post4") & strcmp(StudyDay_np, "CON")

trial5_hc=strcmp(trial_np,"Post5-1") & strcmp(StudyDay_np, "HC")
trial5_or=strcmp(trial_np,"Post5-1") & strcmp(StudyDay_np, "OR")
trial5_od=strcmp(trial_np,"Post5-1") & strcmp(StudyDay_np, "OD")
trial5_con=strcmp(trial_np,"Post5-1") & strcmp(StudyDay_np, "CON")

trial6_hc=strcmp(trial_np,"Post5-2") & strcmp(StudyDay_np, "HC")
trial6_or=strcmp(trial_np,"Post5-2") & strcmp(StudyDay_np, "OR")
trial6_od=strcmp(trial_np,"Post5-2") & strcmp(StudyDay_np, "OD")
trial6_con=strcmp(trial_np,"Post5-2") & strcmp(StudyDay_np, "CON")

trial7_hc=strcmp(trial_np,"Post5-3") & strcmp(StudyDay_np, "HC")
trial7_or=strcmp(trial_np,"Post5-3") & strcmp(StudyDay_np, "OR")
trial7_od=strcmp(trial_np,"Post5-3") & strcmp(StudyDay_np, "OD")
trial7_con=strcmp(trial_np,"Post5-3") & strcmp(StudyDay_np, "CON")

trial8_hc=strcmp(trial_np,"Post5-4") & strcmp(StudyDay_np, "HC")
trial8_or=strcmp(trial_np,"Post5-4") & strcmp(StudyDay_np, "OR")
trial8_od=strcmp(trial_np,"Post5-4") & strcmp(StudyDay_np, "OD")
trial8_con=strcmp(trial_np,"Post5-4") & strcmp(StudyDay_np, "CON")



# %% OS
string="VEH"
studyday=strcmp(StudyDay_np, "HC")
st1=strcmp(StudyDay_np, "OR")
st2=strcmp(StudyDay_np, "OD")
st3=strcmp(StudyDay_np, "CON")
treatment=strcmp(treatment_np, string)

logicresult_hc=trial_hc*treatment;
logicresult_or=trial_or*treatment;
logicresult_od=trial_od*treatment;
logicresult_con=trial_con*treatment;

logicresult_1hc=trial1_hc*treatment;
logicresult_1or=trial1_or*treatment;
logicresult_1od=trial1_od*treatment;
logicresult_1con=trial1_con*treatment;

logicresult_2hc=trial2_hc*treatment;
logicresult_2or=trial2_or*treatment;
logicresult_2od=trial2_od*treatment;
logicresult_2con=trial2_con*treatment;

logicresult_3hc=trial3_hc*treatment;
logicresult_3or=trial3_or*treatment;
logicresult_3od=trial3_od*treatment;
logicresult_3con=trial3_con*treatment;

logicresult_4hc=trial4_hc*treatment;
logicresult_4or=trial4_or*treatment;
logicresult_4od=trial4_od*treatment;
logicresult_4con=trial4_con*treatment;

logicresult_5hc=trial5_hc*treatment;
logicresult_5or=trial5_or*treatment;
logicresult_5od=trial5_od*treatment;
logicresult_5con=trial5_con*treatment;

logicresult_6hc=trial6_hc*treatment;
logicresult_6or=trial6_or*treatment;
logicresult_6od=trial6_od*treatment;
logicresult_6con=trial6_con*treatment;

logicresult_7hc=trial7_hc*treatment;
logicresult_7or=trial7_or*treatment;
logicresult_7od=trial7_od*treatment;
logicresult_7con=trial7_con*treatment;

logicresult_8hc=trial8_hc*treatment;
logicresult_8or=trial8_or*treatment;
logicresult_8od=trial8_od*treatment;
logicresult_8con=trial8_con*treatment;



L_hc=binary_feature(Ripples,logicresult_hc)  
L_or=binary_feature(Ripples,logicresult_or) 
L_od=binary_feature(Ripples,logicresult_od) 
L_con=binary_feature(Ripples,logicresult_con) 

L_1hc=binary_feature(Ripples,logicresult_1hc)  
L_1or=binary_feature(Ripples,logicresult_1or) 
L_1od=binary_feature(Ripples,logicresult_1od) 
L_1con=binary_feature(Ripples,logicresult_1con) 

L_2hc=binary_feature(Ripples,logicresult_2hc)  
L_2or=binary_feature(Ripples,logicresult_2or) 
L_2od=binary_feature(Ripples,logicresult_2od) 
L_2con=binary_feature(Ripples,logicresult_2con) 

L_3hc=binary_feature(Ripples,logicresult_3hc)  
L_3or=binary_feature(Ripples,logicresult_3or) 
L_3od=binary_feature(Ripples,logicresult_3od) 
L_3con=binary_feature(Ripples,logicresult_3con) 

L_4hc=binary_feature(Ripples,logicresult_4hc)  
L_4or=binary_feature(Ripples,logicresult_4or) 
L_4od=binary_feature(Ripples,logicresult_4od) 
L_4con=binary_feature(Ripples,logicresult_4con) 

L_5hc=binary_feature(Ripples,logicresult_5hc)  
L_5or=binary_feature(Ripples,logicresult_5or) 
L_5od=binary_feature(Ripples,logicresult_5od) 
L_5con=binary_feature(Ripples,logicresult_5con) 

L_6hc=binary_feature(Ripples,logicresult_6hc)  
L_6or=binary_feature(Ripples,logicresult_6or) 
L_6od=binary_feature(Ripples,logicresult_6od) 
L_6con=binary_feature(Ripples,logicresult_6con) 

L_7hc=binary_feature(Ripples,logicresult_7hc)  
L_7or=binary_feature(Ripples,logicresult_7or) 
L_7od=binary_feature(Ripples,logicresult_7od) 
L_7con=binary_feature(Ripples,logicresult_7con) 

L_8hc=binary_feature(Ripples,logicresult_8hc)  
L_8or=binary_feature(Ripples,logicresult_8or) 
L_8od=binary_feature(Ripples,logicresult_8od) 
L_8con=binary_feature(Ripples,logicresult_8con) 




fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_hc,0], u[L_hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_hc,0], axis=0)
by1=np.mean(u[L_hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_or,0], u[L_or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_or,0], axis=0)
by1=np.mean(u[L_or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_od,0], u[L_od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_od,0], axis=0)
by1=np.mean(u[L_od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_con,0], u[L_con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_con,0], axis=0)
by1=np.mean(u[L_con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Presleep')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_1hc,0], u[L_1hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_1hc,0], axis=0)
by1=np.mean(u[L_1hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_1or,0], u[L_1or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_1or,0], axis=0)
by1=np.mean(u[L_1or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_1od,0], u[L_1od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_1od,0], axis=0)
by1=np.mean(u[L_1od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_1con,0], u[L_1con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_1con,0], axis=0)
by1=np.mean(u[L_1con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 1')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_2hc,0], u[L_2hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_2hc,0], axis=0)
by1=np.mean(u[L_2hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_2or,0], u[L_2or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_2or,0], axis=0)
by1=np.mean(u[L_2or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_2od,0], u[L_2od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_2od,0], axis=0)
by1=np.mean(u[L_2od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_2con,0], u[L_2con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_2con,0], axis=0)
by1=np.mean(u[L_2con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 2')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_3hc,0], u[L_3hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_3hc,0], axis=0)
by1=np.mean(u[L_3hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_3or,0], u[L_3or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_3or,0], axis=0)
by1=np.mean(u[L_3or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_3od,0], u[L_3od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_3od,0], axis=0)
by1=np.mean(u[L_3od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_3con,0], u[L_3con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_3con,0], axis=0)
by1=np.mean(u[L_3con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 3')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_4hc,0], u[L_4hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_4hc,0], axis=0)
by1=np.mean(u[L_4hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_4or,0], u[L_4or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_4or,0], axis=0)
by1=np.mean(u[L_4or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_4od,0], u[L_4od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_4od,0], axis=0)
by1=np.mean(u[L_4od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_4con,0], u[L_4con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_4con,0], axis=0)
by1=np.mean(u[L_4con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 4')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_5hc,0], u[L_5hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_5hc,0], axis=0)
by1=np.mean(u[L_5hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_5or,0], u[L_5or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_5or,0], axis=0)
by1=np.mean(u[L_5or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_5od,0], u[L_5od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_5od,0], axis=0)
by1=np.mean(u[L_5od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_5con,0], u[L_5con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_5con,0], axis=0)
by1=np.mean(u[L_5con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 5-1')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_6hc,0], u[L_6hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_6hc,0], axis=0)
by1=np.mean(u[L_6hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_6or,0], u[L_6or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_6or,0], axis=0)
by1=np.mean(u[L_6or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_6od,0], u[L_6od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_6od,0], axis=0)
by1=np.mean(u[L_6od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_6con,0], u[L_6con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_6con,0], axis=0)
by1=np.mean(u[L_6con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 5-2')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_7hc,0], u[L_7hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_7hc,0], axis=0)
by1=np.mean(u[L_7hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_7or,0], u[L_7or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_7or,0], axis=0)
by1=np.mean(u[L_7or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_7od,0], u[L_7od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_7od,0], axis=0)
by1=np.mean(u[L_7od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_7con,0], u[L_7con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_7con,0], axis=0)
by1=np.mean(u[L_7con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 5-3')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()




fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_8hc,0], u[L_8hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_8hc,0], axis=0)
by1=np.mean(u[L_8hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_8or,0], u[L_8or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_8or,0], axis=0)
by1=np.mean(u[L_8or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_8od,0], u[L_8od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_8od,0], axis=0)
by1=np.mean(u[L_8od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_8con,0], u[L_8con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_8con,0], axis=0)
by1=np.mean(u[L_8con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 5-4')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


plt.show()


# %% Homecage
string="RGS14"

studyday=strcmp(StudyDay_np, "HC")
st1=strcmp(StudyDay_np, "OR")
st2=strcmp(StudyDay_np, "OD")
st3=strcmp(StudyDay_np, "CON")
treatment=strcmp(treatment_np, string)


logicresult_hc=trial_hc*treatment;
logicresult_or=trial_or*treatment;
logicresult_od=trial_od*treatment;
logicresult_con=trial_con*treatment;

logicresult_1hc=trial1_hc*treatment;
logicresult_1or=trial1_or*treatment;
logicresult_1od=trial1_od*treatment;
logicresult_1con=trial1_con*treatment;

logicresult_2hc=trial2_hc*treatment;
logicresult_2or=trial2_or*treatment;
logicresult_2od=trial2_od*treatment;
logicresult_2con=trial2_con*treatment;

logicresult_3hc=trial3_hc*treatment;
logicresult_3or=trial3_or*treatment;
logicresult_3od=trial3_od*treatment;
logicresult_3con=trial3_con*treatment;

logicresult_4hc=trial4_hc*treatment;
logicresult_4or=trial4_or*treatment;
logicresult_4od=trial4_od*treatment;
logicresult_4con=trial4_con*treatment;

logicresult_5hc=trial5_hc*treatment;
logicresult_5or=trial5_or*treatment;
logicresult_5od=trial5_od*treatment;
logicresult_5con=trial5_con*treatment;

logicresult_6hc=trial6_hc*treatment;
logicresult_6or=trial6_or*treatment;
logicresult_6od=trial6_od*treatment;
logicresult_6con=trial6_con*treatment;

logicresult_7hc=trial7_hc*treatment;
logicresult_7or=trial7_or*treatment;
logicresult_7od=trial7_od*treatment;
logicresult_7con=trial7_con*treatment;

logicresult_8hc=trial8_hc*treatment;
logicresult_8or=trial8_or*treatment;
logicresult_8od=trial8_od*treatment;
logicresult_8con=trial8_con*treatment;



L_hc=binary_feature(Ripples,logicresult_hc)  
L_or=binary_feature(Ripples,logicresult_or) 
L_od=binary_feature(Ripples,logicresult_od) 
L_con=binary_feature(Ripples,logicresult_con) 


L_1hc=binary_feature(Ripples,logicresult_1hc)  
L_1or=binary_feature(Ripples,logicresult_1or) 
L_1od=binary_feature(Ripples,logicresult_1od) 
L_1con=binary_feature(Ripples,logicresult_1con) 

L_2hc=binary_feature(Ripples,logicresult_2hc)  
L_2or=binary_feature(Ripples,logicresult_2or) 
L_2od=binary_feature(Ripples,logicresult_2od) 
L_2con=binary_feature(Ripples,logicresult_2con) 

L_3hc=binary_feature(Ripples,logicresult_3hc)  
L_3or=binary_feature(Ripples,logicresult_3or) 
L_3od=binary_feature(Ripples,logicresult_3od) 
L_3con=binary_feature(Ripples,logicresult_3con) 

L_4hc=binary_feature(Ripples,logicresult_4hc)  
L_4or=binary_feature(Ripples,logicresult_4or) 
L_4od=binary_feature(Ripples,logicresult_4od) 
L_4con=binary_feature(Ripples,logicresult_4con) 

L_5hc=binary_feature(Ripples,logicresult_5hc)  
L_5or=binary_feature(Ripples,logicresult_5or) 
L_5od=binary_feature(Ripples,logicresult_5od) 
L_5con=binary_feature(Ripples,logicresult_5con) 

L_6hc=binary_feature(Ripples,logicresult_6hc)  
L_6or=binary_feature(Ripples,logicresult_6or) 
L_6od=binary_feature(Ripples,logicresult_6od) 
L_6con=binary_feature(Ripples,logicresult_6con) 

L_7hc=binary_feature(Ripples,logicresult_7hc)  
L_7or=binary_feature(Ripples,logicresult_7or) 
L_7od=binary_feature(Ripples,logicresult_7od) 
L_7con=binary_feature(Ripples,logicresult_7con) 

L_8hc=binary_feature(Ripples,logicresult_8hc)  
L_8or=binary_feature(Ripples,logicresult_8or) 
L_8od=binary_feature(Ripples,logicresult_8od) 
L_8con=binary_feature(Ripples,logicresult_8con) 



fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_hc,0], u[L_hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_hc,0], axis=0)
by1=np.mean(u[L_hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_or,0], u[L_or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_or,0], axis=0)
by1=np.mean(u[L_or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_1od,0], u[L_1od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_od,0], axis=0)
by1=np.mean(u[L_od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_con,0], u[L_con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_con,0], axis=0)
by1=np.mean(u[L_con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Presleep')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_1hc,0], u[L_1hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_1hc,0], axis=0)
by1=np.mean(u[L_1hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_1or,0], u[L_1or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_1or,0], axis=0)
by1=np.mean(u[L_1or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_1od,0], u[L_1od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_1od,0], axis=0)
by1=np.mean(u[L_1od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_1con,0], u[L_1con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_1con,0], axis=0)
by1=np.mean(u[L_1con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 1')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_2hc,0], u[L_2hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_2hc,0], axis=0)
by1=np.mean(u[L_2hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_2or,0], u[L_2or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_2or,0], axis=0)
by1=np.mean(u[L_2or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_2od,0], u[L_2od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_2od,0], axis=0)
by1=np.mean(u[L_2od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_2con,0], u[L_2con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_2con,0], axis=0)
by1=np.mean(u[L_2con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 2')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_3hc,0], u[L_3hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_3hc,0], axis=0)
by1=np.mean(u[L_3hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_3or,0], u[L_3or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_3or,0], axis=0)
by1=np.mean(u[L_3or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_3od,0], u[L_3od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_3od,0], axis=0)
by1=np.mean(u[L_3od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_3con,0], u[L_3con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_3con,0], axis=0)
by1=np.mean(u[L_3con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 3')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_4hc,0], u[L_4hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_4hc,0], axis=0)
by1=np.mean(u[L_4hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_4or,0], u[L_4or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_4or,0], axis=0)
by1=np.mean(u[L_4or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_4od,0], u[L_4od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_4od,0], axis=0)
by1=np.mean(u[L_4od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_4con,0], u[L_4con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_4con,0], axis=0)
by1=np.mean(u[L_4con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 4')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_5hc,0], u[L_5hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_5hc,0], axis=0)
by1=np.mean(u[L_5hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_5or,0], u[L_5or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_5or,0], axis=0)
by1=np.mean(u[L_5or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_5od,0], u[L_5od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_5od,0], axis=0)
by1=np.mean(u[L_5od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_5con,0], u[L_5con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_5con,0], axis=0)
by1=np.mean(u[L_5con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 5-1')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_6hc,0], u[L_6hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_6hc,0], axis=0)
by1=np.mean(u[L_6hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_6or,0], u[L_6or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_6or,0], axis=0)
by1=np.mean(u[L_6or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_6od,0], u[L_6od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_6od,0], axis=0)
by1=np.mean(u[L_6od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_6con,0], u[L_6con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_6con,0], axis=0)
by1=np.mean(u[L_6con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 5-2')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_7hc,0], u[L_7hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_7hc,0], axis=0)
by1=np.mean(u[L_7hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_7or,0], u[L_7or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_7or,0], axis=0)
by1=np.mean(u[L_7or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_7od,0], u[L_7od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_7od,0], axis=0)
by1=np.mean(u[L_7od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_7con,0], u[L_7con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_7con,0], axis=0)
by1=np.mean(u[L_7con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 5-3')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()


fig, ax = plt.subplots(figsize=(30,15))

hist1hc=plt.hist2d(u[L_8hc,0], u[L_8hc,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Reds')
ax1=np.mean(u[L_8hc,0], axis=0)
by1=np.mean(u[L_8hc,1], axis=0)
plt.plot(ax1,by1,'ro',markersize=20)

hist1or=plt.hist2d(u[L_8or,0], u[L_8or,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greens')
ax1=np.mean(u[L_8or,0], axis=0)
by1=np.mean(u[L_8or,1], axis=0)
plt.plot(ax1,by1,'bo',markersize=20)

hist1od=plt.hist2d(u[L_8od,0], u[L_8od,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Blues')
ax1=np.mean(u[L_8od,0], axis=0)
by1=np.mean(u[L_8od,1], axis=0)
plt.plot(ax1,by1,'go',markersize=20)

hist1con=plt.hist2d(u[L_8con,0], u[L_8con,1],150,density=1,cmin=0.05, cmax=0.5, vmin=0.05, vmax=0.5, cmap='Greys')
ax1=np.mean(u[L_8con,0], axis=0)
by1=np.mean(u[L_8con,1], axis=0)
plt.plot(ax1,by1,'ko',markersize=20)

plt.colorbar(hist1hc[3], orientation='vertical').set_label('HC', loc='bottom')
plt.colorbar(hist1or[3],orientation='vertical').set_label('OR', loc='bottom')
plt.colorbar(hist1od[3],orientation='vertical').set_label('OD', loc='bottom')
plt.colorbar(hist1con[3],orientation='vertical').set_label('CON', loc='bottom')

plt.title(string+ ' Post Trial 5-4')
plt.xlim([0, 10])
plt.ylim([0, 8])
plt.tight_layout()

plt.show()

