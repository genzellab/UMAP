import os
import sys
os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');
#sys.path.append('/home/genzel/Documents/UMAP')

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


# To be able to compute for RGS14 values, change Rat strings

# %% OS
string="Rat1"
rat=strcmp(rat_np, string)

logicresult_hc=trial_hc*rat;
logicresult_or=trial_or*rat;
logicresult_od=trial_od*rat;
logicresult_con=trial_con*rat;

logicresult_1hc=trial1_hc*rat;
logicresult_1or=trial1_or*rat;
logicresult_1od=trial1_od*rat;
logicresult_1con=trial1_con*rat;

logicresult_2hc=trial2_hc*rat;
logicresult_2or=trial2_or*rat;
logicresult_2od=trial2_od*rat;
logicresult_2con=trial2_con*rat;

logicresult_3hc=trial3_hc*rat;
logicresult_3or=trial3_or*rat;
logicresult_3od=trial3_od*rat;
logicresult_3con=trial3_con*rat;

logicresult_4hc=trial4_hc*rat;
logicresult_4or=trial4_or*rat;
logicresult_4od=trial4_od*rat;
logicresult_4con=trial4_con*rat;

logicresult_5hc=trial5_hc*rat;
logicresult_5or=trial5_or*rat;
logicresult_5od=trial5_od*rat;
logicresult_5con=trial5_con*rat;

logicresult_6hc=trial6_hc*rat;
logicresult_6or=trial6_or*rat;
logicresult_6od=trial6_od*rat;
logicresult_6con=trial6_con*rat;

logicresult_7hc=trial7_hc*rat;
logicresult_7or=trial7_or*rat;
logicresult_7od=trial7_od*rat;
logicresult_7con=trial7_con*rat;

logicresult_8hc=trial8_hc*rat;
logicresult_8or=trial8_or*rat;
logicresult_8od=trial8_od*rat;
logicresult_8con=trial8_con*rat;



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




ax_hc=np.mean(u[L_hc,0], axis=0)
by_hc=np.mean(u[L_hc,1], axis=0)
pre_hc = np.array((ax_hc, by_hc))
pre_hc = pre_hc.flatten()

ax_or=np.mean(u[L_or,0], axis=0)
by_or=np.mean(u[L_or,1], axis=0)
pre_or = np.array((ax_or, by_or))
pre_or = pre_or.flatten()
# Euclidean distance
rat1_dist_prehcor = np.sqrt(np.sum(np.square(pre_hc - pre_or)))

ax_od=np.mean(u[L_od,0], axis=0)
by_od=np.mean(u[L_od,1], axis=0)
pre_od = np.array((ax_od, by_od))
pre_od = pre_od.flatten()
# Euclidean distance
rat1_dist_prehcod = np.sqrt(np.sum(np.square(pre_hc - pre_od)))

ax_con=np.mean(u[L_con,0], axis=0)
by_con=np.mean(u[L_con,1], axis=0)
pre_con = np.array((ax_con, by_con))
pre_con = pre_con.flatten()
# Euclidean distance
rat1_dist_prehccon = np.sqrt(np.sum(np.square(pre_hc - pre_con)))





ax1_hc=np.mean(u[L_1hc,0], axis=0)
by1_hc=np.mean(u[L_1hc,1], axis=0)
pt1_hc = np.array((ax1_hc, by1_hc))
pt1_hc = pt1_hc.flatten()

ax1_or=np.mean(u[L_1or,0], axis=0)
by1_or=np.mean(u[L_1or,1], axis=0)
pt1_or = np.array((ax1_or, by1_or))
pt1_or = pt1_or.flatten()
# Euclidean distance
rat1_dist_pt1hcor = np.sqrt(np.sum(np.square(pt1_hc - pt1_or)))

ax1_od=np.mean(u[L_1od,0], axis=0)
by1_od=np.mean(u[L_1od,1], axis=0)
pt1_od = np.array((ax1_od, by1_od))
pt1_od = pt1_od.flatten()
# Euclidean distance
rat1_dist_pt1hcod = np.sqrt(np.sum(np.square(pt1_hc - pt1_od)))

ax1_con=np.mean(u[L_1con,0], axis=0)
by1_con=np.mean(u[L_1con,1], axis=0)
pt1_con = np.array((ax1_con, by1_con))
pt1_con = pt1_con.flatten()
# Euclidean distance
rat1_dist_pt1hccon = np.sqrt(np.sum(np.square(pt1_hc - pt1_con)))





ax2_hc=np.mean(u[L_2hc,0], axis=0)
by2_hc=np.mean(u[L_2hc,1], axis=0)
pt2_hc = np.array((ax2_hc, by2_hc))
pt2_hc = pt2_hc.flatten()

ax2_or=np.mean(u[L_2or,0], axis=0)
by2_or=np.mean(u[L_2or,1], axis=0)
pt2_or = np.array((ax2_or, by2_or))
pt2_or = pt2_or.flatten()
# Euclidean distance
rat1_dist_pt2hcor = np.sqrt(np.sum(np.square(pt2_hc - pt2_or)))

ax2_od=np.mean(u[L_2od,0], axis=0)
by2_od=np.mean(u[L_2od,1], axis=0)
pt2_od = np.array((ax2_od, by2_od))
pt2_od = pt2_od.flatten()
# Euclidean distance
rat1_dist_pt2hcod = np.sqrt(np.sum(np.square(pt2_hc - pt2_od)))

ax2_con=np.mean(u[L_2con,0], axis=0)
by2_con=np.mean(u[L_2con,1], axis=0)
pt2_con = np.array((ax2_con, by2_con))
pt2_con = pt2_con.flatten()
# Euclidean distance
rat1_dist_pt2hccon = np.sqrt(np.sum(np.square(pt2_hc - pt2_con)))





ax3_hc=np.mean(u[L_3hc,0], axis=0)
by3_hc=np.mean(u[L_3hc,1], axis=0)
pt3_hc = np.array((ax3_hc, by3_hc))
pt3_hc = pt3_hc.flatten()

ax3_or=np.mean(u[L_3or,0], axis=0)
by3_or=np.mean(u[L_3or,1], axis=0)
pt3_or = np.array((ax3_or, by3_or))
pt3_or = pt3_or.flatten()
# Euclidean distance
rat1_dist_pt3hcor = np.sqrt(np.sum(np.square(pt3_hc - pt3_or)))

ax3_od=np.mean(u[L_3od,0], axis=0)
by3_od=np.mean(u[L_3od,1], axis=0)
pt3_od = np.array((ax3_od, by3_od))
pt3_od = pt3_od.flatten()
# Euclidean distance
rat1_dist_pt3hcod = np.sqrt(np.sum(np.square(pt3_hc - pt3_od)))

ax3_con=np.mean(u[L_3con,0], axis=0)
by3_con=np.mean(u[L_3con,1], axis=0)
pt3_con = np.array((ax3_con, by3_con))
pt3_con = pt3_con.flatten()
# Euclidean distance
rat1_dist_pt3hccon = np.sqrt(np.sum(np.square(pt3_hc - pt3_con)))





ax4_hc=np.mean(u[L_4hc,0], axis=0)
by4_hc=np.mean(u[L_4hc,1], axis=0)
pt4_hc = np.array((ax4_hc, by4_hc))
pt4_hc = pt4_hc.flatten()

ax4_or=np.mean(u[L_4or,0], axis=0)
by4_or=np.mean(u[L_4or,1], axis=0)
pt4_or = np.array((ax4_or, by4_or))
pt4_or = pt4_or.flatten()
# Euclidean distance
rat1_dist_pt4hcor = np.sqrt(np.sum(np.square(pt4_hc - pt4_or)))

ax4_od=np.mean(u[L_4od,0], axis=0)
by4_od=np.mean(u[L_4od,1], axis=0)
pt4_od = np.array((ax4_od, by4_od))
pt4_od = pt4_od.flatten()
# Euclidean distance
rat1_dist_pt4hcod = np.sqrt(np.sum(np.square(pt4_hc - pt4_od)))

ax4_con=np.mean(u[L_4con,0], axis=0)
by4_con=np.mean(u[L_4con,1], axis=0)
pt4_con = np.array((ax4_con, by4_con))
pt4_con = pt4_con.flatten()
# Euclidean distance
rat1_dist_pt4hccon = np.sqrt(np.sum(np.square(pt4_hc - pt4_con)))





ax5_hc=np.mean(u[L_5hc,0], axis=0)
by5_hc=np.mean(u[L_5hc,1], axis=0)
pt5_hc = np.array((ax5_hc, by5_hc))
pt5_hc = pt5_hc.flatten()

ax5_or=np.mean(u[L_5or,0], axis=0)
by5_or=np.mean(u[L_5or,1], axis=0)
pt5_or = np.array((ax5_or, by5_or))
pt5_or = pt5_or.flatten()
# Euclidean distance
rat1_dist_pt5hcor = np.sqrt(np.sum(np.square(pt5_hc - pt5_or)))

ax5_od=np.mean(u[L_5od,0], axis=0)
by5_od=np.mean(u[L_5od,1], axis=0)
pt5_od = np.array((ax5_od, by5_od))
pt5_od = pt5_od.flatten()
# Euclidean distance
rat1_dist_pt5hcod = np.sqrt(np.sum(np.square(pt5_hc - pt5_od)))

ax5_con=np.mean(u[L_5con,0], axis=0)
by5_con=np.mean(u[L_5con,1], axis=0)
pt5_con = np.array((ax5_con, by5_con))
pt5_con = pt5_con.flatten()
# Euclidean distance
rat1_dist_pt5hccon = np.sqrt(np.sum(np.square(pt5_hc - pt5_con)))





ax6_hc=np.mean(u[L_6hc,0], axis=0)
by6_hc=np.mean(u[L_6hc,1], axis=0)
pt6_hc = np.array((ax6_hc, by6_hc))
pt6_hc = pt6_hc.flatten()

ax6_or=np.mean(u[L_6or,0], axis=0)
by6_or=np.mean(u[L_6or,1], axis=0)
pt6_or = np.array((ax6_or, by6_or))
pt6_or = pt6_or.flatten()
# Euclidean distance
rat1_dist_pt6hcor = np.sqrt(np.sum(np.square(pt6_hc - pt6_or)))

ax6_od=np.mean(u[L_6od,0], axis=0)
by6_od=np.mean(u[L_6od,1], axis=0)
pt6_od = np.array((ax6_od, by6_od))
pt6_od = pt6_od.flatten()
# Euclidean distance
rat1_dist_pt6hcod = np.sqrt(np.sum(np.square(pt6_hc - pt6_od)))

ax6_con=np.mean(u[L_6con,0], axis=0)
by6_con=np.mean(u[L_6con,1], axis=0)
pt6_con = np.array((ax6_con, by6_con))
pt6_con = pt6_con.flatten()
# Euclidean distance
rat1_dist_pt6hccon = np.sqrt(np.sum(np.square(pt6_hc - pt6_con)))





ax7_hc=np.mean(u[L_7hc,0], axis=0)
by7_hc=np.mean(u[L_7hc,1], axis=0)
pt7_hc = np.array((ax7_hc, by7_hc))
pt7_hc = pt7_hc.flatten()

ax7_or=np.mean(u[L_7or,0], axis=0)
by7_or=np.mean(u[L_7or,1], axis=0)
pt7_or = np.array((ax7_or, by7_or))
pt7_or = pt7_or.flatten()
# Euclidean distance
rat1_dist_pt7hcor = np.sqrt(np.sum(np.square(pt7_hc - pt7_or)))

ax7_od=np.mean(u[L_7od,0], axis=0)
by7_od=np.mean(u[L_7od,1], axis=0)
pt7_od = np.array((ax7_od, by7_od))
pt7_od = pt7_od.flatten()
# Euclidean distance
rat1_dist_pt7hcod = np.sqrt(np.sum(np.square(pt7_hc - pt7_od)))

ax7_con=np.mean(u[L_7con,0], axis=0)
by7_con=np.mean(u[L_7con,1], axis=0)
pt7_con = np.array((ax7_con, by7_con))
pt7_con = pt7_con.flatten()
# Euclidean distance
rat1_dist_pt7hccon = np.sqrt(np.sum(np.square(pt7_hc - pt7_con)))





ax8_hc=np.mean(u[L_8hc,0], axis=0)
by8_hc=np.mean(u[L_8hc,1], axis=0)
pt8_hc = np.array((ax8_hc, by8_hc))
pt8_hc = pt8_hc.flatten()

ax8_or=np.mean(u[L_8or,0], axis=0)
by8_or=np.mean(u[L_8or,1], axis=0)
pt8_or = np.array((ax8_or, by8_or))
pt8_or = pt8_or.flatten()
# Euclidean distance
rat1_dist_pt8hcor = np.sqrt(np.sum(np.square(pt8_hc - pt8_or)))

ax8_od=np.mean(u[L_8od,0], axis=0)
by8_od=np.mean(u[L_8od,1], axis=0)
pt8_od = np.array((ax8_od, by8_od))
pt8_od = pt8_od.flatten()
# Euclidean distance
rat1_dist_pt8hcod = np.sqrt(np.sum(np.square(pt8_hc - pt8_od)))

ax8_con=np.mean(u[L_8con,0], axis=0)
by8_con=np.mean(u[L_8con,1], axis=0)
pt8_con = np.array((ax8_con, by8_con))
pt8_con = pt8_con.flatten()
# Euclidean distance
rat1_dist_pt8hccon = np.sqrt(np.sum(np.square(pt8_hc - pt8_con)))



string="Rat2"
rat=strcmp(rat_np, string)

logicresult_hc=trial_hc*rat;
logicresult_or=trial_or*rat;
logicresult_od=trial_od*rat;
logicresult_con=trial_con*rat;

logicresult_1hc=trial1_hc*rat;
logicresult_1or=trial1_or*rat;
logicresult_1od=trial1_od*rat;
logicresult_1con=trial1_con*rat;

logicresult_2hc=trial2_hc*rat;
logicresult_2or=trial2_or*rat;
logicresult_2od=trial2_od*rat;
logicresult_2con=trial2_con*rat;

logicresult_3hc=trial3_hc*rat;
logicresult_3or=trial3_or*rat;
logicresult_3od=trial3_od*rat;
logicresult_3con=trial3_con*rat;

logicresult_4hc=trial4_hc*rat;
logicresult_4or=trial4_or*rat;
logicresult_4od=trial4_od*rat;
logicresult_4con=trial4_con*rat;

logicresult_5hc=trial5_hc*rat;
logicresult_5or=trial5_or*rat;
logicresult_5od=trial5_od*rat;
logicresult_5con=trial5_con*rat;

logicresult_6hc=trial6_hc*rat;
logicresult_6or=trial6_or*rat;
logicresult_6od=trial6_od*rat;
logicresult_6con=trial6_con*rat;

logicresult_7hc=trial7_hc*rat;
logicresult_7or=trial7_or*rat;
logicresult_7od=trial7_od*rat;
logicresult_7con=trial7_con*rat;

logicresult_8hc=trial8_hc*rat;
logicresult_8or=trial8_or*rat;
logicresult_8od=trial8_od*rat;
logicresult_8con=trial8_con*rat;



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




ax_hc=np.mean(u[L_hc,0], axis=0)
by_hc=np.mean(u[L_hc,1], axis=0)
pre_hc = np.array((ax_hc, by_hc))
pre_hc = pre_hc.flatten()

ax_or=np.mean(u[L_or,0], axis=0)
by_or=np.mean(u[L_or,1], axis=0)
pre_or = np.array((ax_or, by_or))
pre_or = pre_or.flatten()
# Euclidean distance
rat2_dist_prehcor = np.sqrt(np.sum(np.square(pre_hc - pre_or)))

ax_od=np.mean(u[L_od,0], axis=0)
by_od=np.mean(u[L_od,1], axis=0)
pre_od = np.array((ax_od, by_od))
pre_od = pre_od.flatten()
# Euclidean distance
rat2_dist_prehcod = np.sqrt(np.sum(np.square(pre_hc - pre_od)))

ax_con=np.mean(u[L_con,0], axis=0)
by_con=np.mean(u[L_con,1], axis=0)
pre_con = np.array((ax_con, by_con))
pre_con = pre_con.flatten()
# Euclidean distance
rat2_dist_prehccon = np.sqrt(np.sum(np.square(pre_hc - pre_con)))





ax1_hc=np.mean(u[L_1hc,0], axis=0)
by1_hc=np.mean(u[L_1hc,1], axis=0)
pt1_hc = np.array((ax1_hc, by1_hc))
pt1_hc = pt1_hc.flatten()

ax1_or=np.mean(u[L_1or,0], axis=0)
by1_or=np.mean(u[L_1or,1], axis=0)
pt1_or = np.array((ax1_or, by1_or))
pt1_or = pt1_or.flatten()
# Euclidean distance
rat2_dist_pt1hcor = np.sqrt(np.sum(np.square(pt1_hc - pt1_or)))

ax1_od=np.mean(u[L_1od,0], axis=0)
by1_od=np.mean(u[L_1od,1], axis=0)
pt1_od = np.array((ax1_od, by1_od))
pt1_od = pt1_od.flatten()
# Euclidean distance
rat2_dist_pt1hcod = np.sqrt(np.sum(np.square(pt1_hc - pt1_od)))

ax1_con=np.mean(u[L_1con,0], axis=0)
by1_con=np.mean(u[L_1con,1], axis=0)
pt1_con = np.array((ax1_con, by1_con))
pt1_con = pt1_con.flatten()
# Euclidean distance
rat2_dist_pt1hccon = np.sqrt(np.sum(np.square(pt1_hc - pt1_con)))





ax2_hc=np.mean(u[L_2hc,0], axis=0)
by2_hc=np.mean(u[L_2hc,1], axis=0)
pt2_hc = np.array((ax2_hc, by2_hc))
pt2_hc = pt2_hc.flatten()

ax2_or=np.mean(u[L_2or,0], axis=0)
by2_or=np.mean(u[L_2or,1], axis=0)
pt2_or = np.array((ax2_or, by2_or))
pt2_or = pt2_or.flatten()
# Euclidean distance
rat2_dist_pt2hcor = np.sqrt(np.sum(np.square(pt2_hc - pt2_or)))

ax2_od=np.mean(u[L_2od,0], axis=0)
by2_od=np.mean(u[L_2od,1], axis=0)
pt2_od = np.array((ax2_od, by2_od))
pt2_od = pt2_od.flatten()
# Euclidean distance
rat2_dist_pt2hcod = np.sqrt(np.sum(np.square(pt2_hc - pt2_od)))

ax2_con=np.mean(u[L_2con,0], axis=0)
by2_con=np.mean(u[L_2con,1], axis=0)
pt2_con = np.array((ax2_con, by2_con))
pt2_con = pt2_con.flatten()
# Euclidean distance
rat2_dist_pt2hccon = np.sqrt(np.sum(np.square(pt2_hc - pt2_con)))





ax3_hc=np.mean(u[L_3hc,0], axis=0)
by3_hc=np.mean(u[L_3hc,1], axis=0)
pt3_hc = np.array((ax3_hc, by3_hc))
pt3_hc = pt3_hc.flatten()

ax3_or=np.mean(u[L_3or,0], axis=0)
by3_or=np.mean(u[L_3or,1], axis=0)
pt3_or = np.array((ax3_or, by3_or))
pt3_or = pt3_or.flatten()
# Euclidean distance
rat2_dist_pt3hcor = np.sqrt(np.sum(np.square(pt3_hc - pt3_or)))

ax3_od=np.mean(u[L_3od,0], axis=0)
by3_od=np.mean(u[L_3od,1], axis=0)
pt3_od = np.array((ax3_od, by3_od))
pt3_od = pt3_od.flatten()
# Euclidean distance
rat2_dist_pt3hcod = np.sqrt(np.sum(np.square(pt3_hc - pt3_od)))

ax3_con=np.mean(u[L_3con,0], axis=0)
by3_con=np.mean(u[L_3con,1], axis=0)
pt3_con = np.array((ax3_con, by3_con))
pt3_con = pt3_con.flatten()
# Euclidean distance
rat2_dist_pt3hccon = np.sqrt(np.sum(np.square(pt3_hc - pt3_con)))





ax4_hc=np.mean(u[L_4hc,0], axis=0)
by4_hc=np.mean(u[L_4hc,1], axis=0)
pt4_hc = np.array((ax4_hc, by4_hc))
pt4_hc = pt4_hc.flatten()

ax4_or=np.mean(u[L_4or,0], axis=0)
by4_or=np.mean(u[L_4or,1], axis=0)
pt4_or = np.array((ax4_or, by4_or))
pt4_or = pt4_or.flatten()
# Euclidean distance
rat2_dist_pt4hcor = np.sqrt(np.sum(np.square(pt4_hc - pt4_or)))

ax4_od=np.mean(u[L_4od,0], axis=0)
by4_od=np.mean(u[L_4od,1], axis=0)
pt4_od = np.array((ax4_od, by4_od))
pt4_od = pt4_od.flatten()
# Euclidean distance
rat2_dist_pt4hcod = np.sqrt(np.sum(np.square(pt4_hc - pt4_od)))

ax4_con=np.mean(u[L_4con,0], axis=0)
by4_con=np.mean(u[L_4con,1], axis=0)
pt4_con = np.array((ax4_con, by4_con))
pt4_con = pt4_con.flatten()
# Euclidean distance
rat2_dist_pt4hccon = np.sqrt(np.sum(np.square(pt4_hc - pt4_con)))





ax5_hc=np.mean(u[L_5hc,0], axis=0)
by5_hc=np.mean(u[L_5hc,1], axis=0)
pt5_hc = np.array((ax5_hc, by5_hc))
pt5_hc = pt5_hc.flatten()

ax5_or=np.mean(u[L_5or,0], axis=0)
by5_or=np.mean(u[L_5or,1], axis=0)
pt5_or = np.array((ax5_or, by5_or))
pt5_or = pt5_or.flatten()
# Euclidean distance
rat2_dist_pt5hcor = np.sqrt(np.sum(np.square(pt5_hc - pt5_or)))

ax5_od=np.mean(u[L_5od,0], axis=0)
by5_od=np.mean(u[L_5od,1], axis=0)
pt5_od = np.array((ax5_od, by5_od))
pt5_od = pt5_od.flatten()
# Euclidean distance
rat2_dist_pt5hcod = np.sqrt(np.sum(np.square(pt5_hc - pt5_od)))

ax5_con=np.mean(u[L_5con,0], axis=0)
by5_con=np.mean(u[L_5con,1], axis=0)
pt5_con = np.array((ax5_con, by5_con))
pt5_con = pt5_con.flatten()
# Euclidean distance
rat2_dist_pt5hccon = np.sqrt(np.sum(np.square(pt5_hc - pt5_con)))





ax6_hc=np.mean(u[L_6hc,0], axis=0)
by6_hc=np.mean(u[L_6hc,1], axis=0)
pt6_hc = np.array((ax6_hc, by6_hc))
pt6_hc = pt6_hc.flatten()

ax6_or=np.mean(u[L_6or,0], axis=0)
by6_or=np.mean(u[L_6or,1], axis=0)
pt6_or = np.array((ax6_or, by6_or))
pt6_or = pt6_or.flatten()
# Euclidean distance
rat2_dist_pt6hcor = np.sqrt(np.sum(np.square(pt6_hc - pt6_or)))

ax6_od=np.mean(u[L_6od,0], axis=0)
by6_od=np.mean(u[L_6od,1], axis=0)
pt6_od = np.array((ax6_od, by6_od))
pt6_od = pt6_od.flatten()
# Euclidean distance
rat2_dist_pt6hcod = np.sqrt(np.sum(np.square(pt6_hc - pt6_od)))

ax6_con=np.mean(u[L_6con,0], axis=0)
by6_con=np.mean(u[L_6con,1], axis=0)
pt6_con = np.array((ax6_con, by6_con))
pt6_con = pt6_con.flatten()
# Euclidean distance
rat2_dist_pt6hccon = np.sqrt(np.sum(np.square(pt6_hc - pt6_con)))





ax7_hc=np.mean(u[L_7hc,0], axis=0)
by7_hc=np.mean(u[L_7hc,1], axis=0)
pt7_hc = np.array((ax7_hc, by7_hc))
pt7_hc = pt7_hc.flatten()

ax7_or=np.mean(u[L_7or,0], axis=0)
by7_or=np.mean(u[L_7or,1], axis=0)
pt7_or = np.array((ax7_or, by7_or))
pt7_or = pt7_or.flatten()
# Euclidean distance
rat2_dist_pt7hcor = np.sqrt(np.sum(np.square(pt7_hc - pt7_or)))

ax7_od=np.mean(u[L_7od,0], axis=0)
by7_od=np.mean(u[L_7od,1], axis=0)
pt7_od = np.array((ax7_od, by7_od))
pt7_od = pt7_od.flatten()
# Euclidean distance
rat2_dist_pt7hcod = np.sqrt(np.sum(np.square(pt7_hc - pt7_od)))

ax7_con=np.mean(u[L_7con,0], axis=0)
by7_con=np.mean(u[L_7con,1], axis=0)
pt7_con = np.array((ax7_con, by7_con))
pt7_con = pt7_con.flatten()
# Euclidean distance
rat2_dist_pt7hccon = np.sqrt(np.sum(np.square(pt7_hc - pt7_con)))





ax8_hc=np.mean(u[L_8hc,0], axis=0)
by8_hc=np.mean(u[L_8hc,1], axis=0)
pt8_hc = np.array((ax8_hc, by8_hc))
pt8_hc = pt8_hc.flatten()

ax8_or=np.mean(u[L_8or,0], axis=0)
by8_or=np.mean(u[L_8or,1], axis=0)
pt8_or = np.array((ax8_or, by8_or))
pt8_or = pt8_or.flatten()
# Euclidean distance
rat2_dist_pt8hcor = np.sqrt(np.sum(np.square(pt8_hc - pt8_or)))

ax8_od=np.mean(u[L_8od,0], axis=0)
by8_od=np.mean(u[L_8od,1], axis=0)
pt8_od = np.array((ax8_od, by8_od))
pt8_od = pt8_od.flatten()
# Euclidean distance
rat2_dist_pt8hcod = np.sqrt(np.sum(np.square(pt8_hc - pt8_od)))

ax8_con=np.mean(u[L_8con,0], axis=0)
by8_con=np.mean(u[L_8con,1], axis=0)
pt8_con = np.array((ax8_con, by8_con))
pt8_con = pt8_con.flatten()
# Euclidean distance
rat2_dist_pt8hccon = np.sqrt(np.sum(np.square(pt8_hc - pt8_con)))






string="Rat6"
rat=strcmp(rat_np, string)

logicresult_hc=trial_hc*rat;
logicresult_or=trial_or*rat;
logicresult_od=trial_od*rat;
logicresult_con=trial_con*rat;

logicresult_1hc=trial1_hc*rat;
logicresult_1or=trial1_or*rat;
logicresult_1od=trial1_od*rat;
logicresult_1con=trial1_con*rat;

logicresult_2hc=trial2_hc*rat;
logicresult_2or=trial2_or*rat;
logicresult_2od=trial2_od*rat;
logicresult_2con=trial2_con*rat;

logicresult_3hc=trial3_hc*rat;
logicresult_3or=trial3_or*rat;
logicresult_3od=trial3_od*rat;
logicresult_3con=trial3_con*rat;

logicresult_4hc=trial4_hc*rat;
logicresult_4or=trial4_or*rat;
logicresult_4od=trial4_od*rat;
logicresult_4con=trial4_con*rat;

logicresult_5hc=trial5_hc*rat;
logicresult_5or=trial5_or*rat;
logicresult_5od=trial5_od*rat;
logicresult_5con=trial5_con*rat;

logicresult_6hc=trial6_hc*rat;
logicresult_6or=trial6_or*rat;
logicresult_6od=trial6_od*rat;
logicresult_6con=trial6_con*rat;

logicresult_7hc=trial7_hc*rat;
logicresult_7or=trial7_or*rat;
logicresult_7od=trial7_od*rat;
logicresult_7con=trial7_con*rat;

logicresult_8hc=trial8_hc*rat;
logicresult_8or=trial8_or*rat;
logicresult_8od=trial8_od*rat;
logicresult_8con=trial8_con*rat;



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



ax_hc=np.mean(u[L_hc,0], axis=0)
by_hc=np.mean(u[L_hc,1], axis=0)
pre_hc = np.array((ax_hc, by_hc))
pre_hc = pre_hc.flatten()

ax_or=np.mean(u[L_or,0], axis=0)
by_or=np.mean(u[L_or,1], axis=0)
pre_or = np.array((ax_or, by_or))
pre_or = pre_or.flatten()
# Euclidean distance
rat6_dist_prehcor = np.sqrt(np.sum(np.square(pre_hc - pre_or)))

ax_od=np.mean(u[L_od,0], axis=0)
by_od=np.mean(u[L_od,1], axis=0)
pre_od = np.array((ax_od, by_od))
pre_od = pre_od.flatten()
# Euclidean distance
rat6_dist_prehcod = np.sqrt(np.sum(np.square(pre_hc - pre_od)))

ax_con=np.mean(u[L_con,0], axis=0)
by_con=np.mean(u[L_con,1], axis=0)
pre_con = np.array((ax_con, by_con))
pre_con = pre_con.flatten()
# Euclidean distance
rat6_dist_prehccon = np.sqrt(np.sum(np.square(pre_hc - pre_con)))





ax1_hc=np.mean(u[L_1hc,0], axis=0)
by1_hc=np.mean(u[L_1hc,1], axis=0)
pt1_hc = np.array((ax1_hc, by1_hc))
pt1_hc = pt1_hc.flatten()

ax1_or=np.mean(u[L_1or,0], axis=0)
by1_or=np.mean(u[L_1or,1], axis=0)
pt1_or = np.array((ax1_or, by1_or))
pt1_or = pt1_or.flatten()
# Euclidean distance
rat6_dist_pt1hcor = np.sqrt(np.sum(np.square(pt1_hc - pt1_or)))

ax1_od=np.mean(u[L_1od,0], axis=0)
by1_od=np.mean(u[L_1od,1], axis=0)
pt1_od = np.array((ax1_od, by1_od))
pt1_od = pt1_od.flatten()
# Euclidean distance
rat6_dist_pt1hcod = np.sqrt(np.sum(np.square(pt1_hc - pt1_od)))

ax1_con=np.mean(u[L_1con,0], axis=0)
by1_con=np.mean(u[L_1con,1], axis=0)
pt1_con = np.array((ax1_con, by1_con))
pt1_con = pt1_con.flatten()
# Euclidean distance
rat6_dist_pt1hccon = np.sqrt(np.sum(np.square(pt1_hc - pt1_con)))





ax2_hc=np.mean(u[L_2hc,0], axis=0)
by2_hc=np.mean(u[L_2hc,1], axis=0)
pt2_hc = np.array((ax2_hc, by2_hc))
pt2_hc = pt2_hc.flatten()

ax2_or=np.mean(u[L_2or,0], axis=0)
by2_or=np.mean(u[L_2or,1], axis=0)
pt2_or = np.array((ax2_or, by2_or))
pt2_or = pt2_or.flatten()
# Euclidean distance
rat6_dist_pt2hcor = np.sqrt(np.sum(np.square(pt2_hc - pt2_or)))

ax2_od=np.mean(u[L_2od,0], axis=0)
by2_od=np.mean(u[L_2od,1], axis=0)
pt2_od = np.array((ax2_od, by2_od))
pt2_od = pt2_od.flatten()
# Euclidean distance
rat6_dist_pt2hcod = np.sqrt(np.sum(np.square(pt2_hc - pt2_od)))

ax2_con=np.mean(u[L_2con,0], axis=0)
by2_con=np.mean(u[L_2con,1], axis=0)
pt2_con = np.array((ax2_con, by2_con))
pt2_con = pt2_con.flatten()
# Euclidean distance
rat6_dist_pt2hccon = np.sqrt(np.sum(np.square(pt2_hc - pt2_con)))





ax3_hc=np.mean(u[L_3hc,0], axis=0)
by3_hc=np.mean(u[L_3hc,1], axis=0)
pt3_hc = np.array((ax3_hc, by3_hc))
pt3_hc = pt3_hc.flatten()

ax3_or=np.mean(u[L_3or,0], axis=0)
by3_or=np.mean(u[L_3or,1], axis=0)
pt3_or = np.array((ax3_or, by3_or))
pt3_or = pt3_or.flatten()
# Euclidean distance
rat6_dist_pt3hcor = np.sqrt(np.sum(np.square(pt3_hc - pt3_or)))

ax3_od=np.mean(u[L_3od,0], axis=0)
by3_od=np.mean(u[L_3od,1], axis=0)
pt3_od = np.array((ax3_od, by3_od))
pt3_od = pt3_od.flatten()
# Euclidean distance
rat6_dist_pt3hcod = np.sqrt(np.sum(np.square(pt3_hc - pt3_od)))

ax3_con=np.mean(u[L_3con,0], axis=0)
by3_con=np.mean(u[L_3con,1], axis=0)
pt3_con = np.array((ax3_con, by3_con))
pt3_con = pt3_con.flatten()
# Euclidean distance
rat6_dist_pt3hccon = np.sqrt(np.sum(np.square(pt3_hc - pt3_con)))





ax4_hc=np.mean(u[L_4hc,0], axis=0)
by4_hc=np.mean(u[L_4hc,1], axis=0)
pt4_hc = np.array((ax4_hc, by4_hc))
pt4_hc = pt4_hc.flatten()

ax4_or=np.mean(u[L_4or,0], axis=0)
by4_or=np.mean(u[L_4or,1], axis=0)
pt4_or = np.array((ax4_or, by4_or))
pt4_or = pt4_or.flatten()
# Euclidean distance
rat6_dist_pt4hcor = np.sqrt(np.sum(np.square(pt4_hc - pt4_or)))

ax4_od=np.mean(u[L_4od,0], axis=0)
by4_od=np.mean(u[L_4od,1], axis=0)
pt4_od = np.array((ax4_od, by4_od))
pt4_od = pt4_od.flatten()
# Euclidean distance
rat6_dist_pt4hcod = np.sqrt(np.sum(np.square(pt4_hc - pt4_od)))

ax4_con=np.mean(u[L_4con,0], axis=0)
by4_con=np.mean(u[L_4con,1], axis=0)
pt4_con = np.array((ax4_con, by4_con))
pt4_con = pt4_con.flatten()
# Euclidean distance
rat6_dist_pt4hccon = np.sqrt(np.sum(np.square(pt4_hc - pt4_con)))





ax5_hc=np.mean(u[L_5hc,0], axis=0)
by5_hc=np.mean(u[L_5hc,1], axis=0)
pt5_hc = np.array((ax5_hc, by5_hc))
pt5_hc = pt5_hc.flatten()

ax5_or=np.mean(u[L_5or,0], axis=0)
by5_or=np.mean(u[L_5or,1], axis=0)
pt5_or = np.array((ax5_or, by5_or))
pt5_or = pt5_or.flatten()
# Euclidean distance
rat6_dist_pt5hcor = np.sqrt(np.sum(np.square(pt5_hc - pt5_or)))

ax5_od=np.mean(u[L_5od,0], axis=0)
by5_od=np.mean(u[L_5od,1], axis=0)
pt5_od = np.array((ax5_od, by5_od))
pt5_od = pt5_od.flatten()
# Euclidean distance
rat6_dist_pt5hcod = np.sqrt(np.sum(np.square(pt5_hc - pt5_od)))

ax5_con=np.mean(u[L_5con,0], axis=0)
by5_con=np.mean(u[L_5con,1], axis=0)
pt5_con = np.array((ax5_con, by5_con))
pt5_con = pt5_con.flatten()
# Euclidean distance
rat6_dist_pt5hccon = np.sqrt(np.sum(np.square(pt5_hc - pt5_con)))





ax6_hc=np.mean(u[L_6hc,0], axis=0)
by6_hc=np.mean(u[L_6hc,1], axis=0)
pt6_hc = np.array((ax6_hc, by6_hc))
pt6_hc = pt6_hc.flatten()

ax6_or=np.mean(u[L_6or,0], axis=0)
by6_or=np.mean(u[L_6or,1], axis=0)
pt6_or = np.array((ax6_or, by6_or))
pt6_or = pt6_or.flatten()
# Euclidean distance
rat6_dist_pt6hcor = np.sqrt(np.sum(np.square(pt6_hc - pt6_or)))

ax6_od=np.mean(u[L_6od,0], axis=0)
by6_od=np.mean(u[L_6od,1], axis=0)
pt6_od = np.array((ax6_od, by6_od))
pt6_od = pt6_od.flatten()
# Euclidean distance
rat6_dist_pt6hcod = np.sqrt(np.sum(np.square(pt6_hc - pt6_od)))

ax6_con=np.mean(u[L_6con,0], axis=0)
by6_con=np.mean(u[L_6con,1], axis=0)
pt6_con = np.array((ax6_con, by6_con))
pt6_con = pt6_con.flatten()
# Euclidean distance
rat6_dist_pt6hccon = np.sqrt(np.sum(np.square(pt6_hc - pt6_con)))





ax7_hc=np.mean(u[L_7hc,0], axis=0)
by7_hc=np.mean(u[L_7hc,1], axis=0)
pt7_hc = np.array((ax7_hc, by7_hc))
pt7_hc = pt7_hc.flatten()

ax7_or=np.mean(u[L_7or,0], axis=0)
by7_or=np.mean(u[L_7or,1], axis=0)
pt7_or = np.array((ax7_or, by7_or))
pt7_or = pt7_or.flatten()
# Euclidean distance
rat6_dist_pt7hcor = np.sqrt(np.sum(np.square(pt7_hc - pt7_or)))

ax7_od=np.mean(u[L_7od,0], axis=0)
by7_od=np.mean(u[L_7od,1], axis=0)
pt7_od = np.array((ax7_od, by7_od))
pt7_od = pt7_od.flatten()
# Euclidean distance
rat6_dist_pt7hcod = np.sqrt(np.sum(np.square(pt7_hc - pt7_od)))

ax7_con=np.mean(u[L_7con,0], axis=0)
by7_con=np.mean(u[L_7con,1], axis=0)
pt7_con = np.array((ax7_con, by7_con))
pt7_con = pt7_con.flatten()
# Euclidean distance
rat6_dist_pt7hccon = np.sqrt(np.sum(np.square(pt7_hc - pt7_con)))





ax8_hc=np.mean(u[L_8hc,0], axis=0)
by8_hc=np.mean(u[L_8hc,1], axis=0)
pt8_hc = np.array((ax8_hc, by8_hc))
pt8_hc = pt8_hc.flatten()

ax8_or=np.mean(u[L_8or,0], axis=0)
by8_or=np.mean(u[L_8or,1], axis=0)
pt8_or = np.array((ax8_or, by8_or))
pt8_or = pt8_or.flatten()
# Euclidean distance
rat6_dist_pt8hcor = np.sqrt(np.sum(np.square(pt8_hc - pt8_or)))

ax8_od=np.mean(u[L_8od,0], axis=0)
by8_od=np.mean(u[L_8od,1], axis=0)
pt8_od = np.array((ax8_od, by8_od))
pt8_od = pt8_od.flatten()
# Euclidean distance
rat6_dist_pt8hcod = np.sqrt(np.sum(np.square(pt8_hc - pt8_od)))

ax8_con=np.mean(u[L_8con,0], axis=0)
by8_con=np.mean(u[L_8con,1], axis=0)
pt8_con = np.array((ax8_con, by8_con))
pt8_con = pt8_con.flatten()
# Euclidean distance
rat6_dist_pt8hccon = np.sqrt(np.sum(np.square(pt8_hc - pt8_con)))







string="Rat9"
rat=strcmp(rat_np, string)

logicresult_hc=trial_hc*rat;
logicresult_or=trial_or*rat;
logicresult_od=trial_od*rat;
logicresult_con=trial_con*rat;

logicresult_1hc=trial1_hc*rat;
logicresult_1or=trial1_or*rat;
logicresult_1od=trial1_od*rat;
logicresult_1con=trial1_con*rat;

logicresult_2hc=trial2_hc*rat;
logicresult_2or=trial2_or*rat;
logicresult_2od=trial2_od*rat;
logicresult_2con=trial2_con*rat;

logicresult_3hc=trial3_hc*rat;
logicresult_3or=trial3_or*rat;
logicresult_3od=trial3_od*rat;
logicresult_3con=trial3_con*rat;

logicresult_4hc=trial4_hc*rat;
logicresult_4or=trial4_or*rat;
logicresult_4od=trial4_od*rat;
logicresult_4con=trial4_con*rat;

logicresult_5hc=trial5_hc*rat;
logicresult_5or=trial5_or*rat;
logicresult_5od=trial5_od*rat;
logicresult_5con=trial5_con*rat;

logicresult_6hc=trial6_hc*rat;
logicresult_6or=trial6_or*rat;
logicresult_6od=trial6_od*rat;
logicresult_6con=trial6_con*rat;

logicresult_7hc=trial7_hc*rat;
logicresult_7or=trial7_or*rat;
logicresult_7od=trial7_od*rat;
logicresult_7con=trial7_con*rat;

logicresult_8hc=trial8_hc*rat;
logicresult_8or=trial8_or*rat;
logicresult_8od=trial8_od*rat;
logicresult_8con=trial8_con*rat;



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


ax_hc=np.mean(u[L_hc,0], axis=0)
by_hc=np.mean(u[L_hc,1], axis=0)
pre_hc = np.array((ax_hc, by_hc))
pre_hc = pre_hc.flatten()

ax_or=np.mean(u[L_or,0], axis=0)
by_or=np.mean(u[L_or,1], axis=0)
pre_or = np.array((ax_or, by_or))
pre_or = pre_or.flatten()
# Euclidean distance
rat9_dist_prehcor = np.sqrt(np.sum(np.square(pre_hc - pre_or)))

ax_od=np.mean(u[L_od,0], axis=0)
by_od=np.mean(u[L_od,1], axis=0)
pre_od = np.array((ax_od, by_od))
pre_od = pre_od.flatten()
# Euclidean distance
rat9_dist_prehcod = np.sqrt(np.sum(np.square(pre_hc - pre_od)))

ax_con=np.mean(u[L_con,0], axis=0)
by_con=np.mean(u[L_con,1], axis=0)
pre_con = np.array((ax_con, by_con))
pre_con = pre_con.flatten()
# Euclidean distance
rat9_dist_prehccon = np.sqrt(np.sum(np.square(pre_hc - pre_con)))

ax1_hc=np.mean(u[L_1hc,0], axis=0)
by1_hc=np.mean(u[L_1hc,1], axis=0)
pt1_hc = np.array((ax1_hc, by1_hc))
pt1_hc = pt1_hc.flatten()

ax1_or=np.mean(u[L_1or,0], axis=0)
by1_or=np.mean(u[L_1or,1], axis=0)
pt1_or = np.array((ax1_or, by1_or))
pt1_or = pt1_or.flatten()
# Euclidean distance
rat9_dist_pt1hcor = np.sqrt(np.sum(np.square(pt1_hc - pt1_or)))

ax1_od=np.mean(u[L_1od,0], axis=0)
by1_od=np.mean(u[L_1od,1], axis=0)
pt1_od = np.array((ax1_od, by1_od))
pt1_od = pt1_od.flatten()
# Euclidean distance
rat9_dist_pt1hcod = np.sqrt(np.sum(np.square(pt1_hc - pt1_od)))

ax1_con=np.mean(u[L_1con,0], axis=0)
by1_con=np.mean(u[L_1con,1], axis=0)
pt1_con = np.array((ax1_con, by1_con))
pt1_con = pt1_con.flatten()
# Euclidean distance
rat9_dist_pt1hccon = np.sqrt(np.sum(np.square(pt1_hc - pt1_con)))





ax2_hc=np.mean(u[L_2hc,0], axis=0)
by2_hc=np.mean(u[L_2hc,1], axis=0)
pt2_hc = np.array((ax2_hc, by2_hc))
pt2_hc = pt2_hc.flatten()

ax2_or=np.mean(u[L_2or,0], axis=0)
by2_or=np.mean(u[L_2or,1], axis=0)
pt2_or = np.array((ax2_or, by2_or))
pt2_or = pt2_or.flatten()
# Euclidean distance
rat9_dist_pt2hcor = np.sqrt(np.sum(np.square(pt2_hc - pt2_or)))

ax2_od=np.mean(u[L_2od,0], axis=0)
by2_od=np.mean(u[L_2od,1], axis=0)
pt2_od = np.array((ax2_od, by2_od))
pt2_od = pt2_od.flatten()
# Euclidean distance
rat9_dist_pt2hcod = np.sqrt(np.sum(np.square(pt2_hc - pt2_od)))

ax2_con=np.mean(u[L_2con,0], axis=0)
by2_con=np.mean(u[L_2con,1], axis=0)
pt2_con = np.array((ax2_con, by2_con))
pt2_con = pt2_con.flatten()
# Euclidean distance
rat9_dist_pt2hccon = np.sqrt(np.sum(np.square(pt2_hc - pt2_con)))





ax3_hc=np.mean(u[L_3hc,0], axis=0)
by3_hc=np.mean(u[L_3hc,1], axis=0)
pt3_hc = np.array((ax3_hc, by3_hc))
pt3_hc = pt3_hc.flatten()

ax3_or=np.mean(u[L_3or,0], axis=0)
by3_or=np.mean(u[L_3or,1], axis=0)
pt3_or = np.array((ax3_or, by3_or))
pt3_or = pt3_or.flatten()
# Euclidean distance
rat9_dist_pt3hcor = np.sqrt(np.sum(np.square(pt3_hc - pt3_or)))

ax3_od=np.mean(u[L_3od,0], axis=0)
by3_od=np.mean(u[L_3od,1], axis=0)
pt3_od = np.array((ax3_od, by3_od))
pt3_od = pt3_od.flatten()
# Euclidean distance
rat9_dist_pt3hcod = np.sqrt(np.sum(np.square(pt3_hc - pt3_od)))

ax3_con=np.mean(u[L_3con,0], axis=0)
by3_con=np.mean(u[L_3con,1], axis=0)
pt3_con = np.array((ax3_con, by3_con))
pt3_con = pt3_con.flatten()
# Euclidean distance
rat9_dist_pt3hccon = np.sqrt(np.sum(np.square(pt3_hc - pt3_con)))

ax4_hc=np.mean(u[L_4hc,0], axis=0)
by4_hc=np.mean(u[L_4hc,1], axis=0)
pt4_hc = np.array((ax4_hc, by4_hc))
pt4_hc = pt4_hc.flatten()

ax4_or=np.mean(u[L_4or,0], axis=0)
by4_or=np.mean(u[L_4or,1], axis=0)
pt4_or = np.array((ax4_or, by4_or))
pt4_or = pt4_or.flatten()
# Euclidean distance
rat9_dist_pt4hcor = np.sqrt(np.sum(np.square(pt4_hc - pt4_or)))

ax4_od=np.mean(u[L_4od,0], axis=0)
by4_od=np.mean(u[L_4od,1], axis=0)
pt4_od = np.array((ax4_od, by4_od))
pt4_od = pt4_od.flatten()
# Euclidean distance
rat9_dist_pt4hcod = np.sqrt(np.sum(np.square(pt4_hc - pt4_od)))

ax4_con=np.mean(u[L_4con,0], axis=0)
by4_con=np.mean(u[L_4con,1], axis=0)
pt4_con = np.array((ax4_con, by4_con))
pt4_con = pt4_con.flatten()
# Euclidean distance
rat9_dist_pt4hccon = np.sqrt(np.sum(np.square(pt4_hc - pt4_con)))





ax5_hc=np.mean(u[L_5hc,0], axis=0)
by5_hc=np.mean(u[L_5hc,1], axis=0)
pt5_hc = np.array((ax5_hc, by5_hc))
pt5_hc = pt5_hc.flatten()

ax5_or=np.mean(u[L_5or,0], axis=0)
by5_or=np.mean(u[L_5or,1], axis=0)
pt5_or = np.array((ax5_or, by5_or))
pt5_or = pt5_or.flatten()
# Euclidean distance
rat9_dist_pt5hcor = np.sqrt(np.sum(np.square(pt5_hc - pt5_or)))

ax5_od=np.mean(u[L_5od,0], axis=0)
by5_od=np.mean(u[L_5od,1], axis=0)
pt5_od = np.array((ax5_od, by5_od))
pt5_od = pt5_od.flatten()
# Euclidean distance
rat9_dist_pt5hcod = np.sqrt(np.sum(np.square(pt5_hc - pt5_od)))

ax5_con=np.mean(u[L_5con,0], axis=0)
by5_con=np.mean(u[L_5con,1], axis=0)
pt5_con = np.array((ax5_con, by5_con))
pt5_con = pt5_con.flatten()
# Euclidean distance
rat9_dist_pt5hccon = np.sqrt(np.sum(np.square(pt5_hc - pt5_con)))





ax6_hc=np.mean(u[L_6hc,0], axis=0)
by6_hc=np.mean(u[L_6hc,1], axis=0)
pt6_hc = np.array((ax6_hc, by6_hc))
pt6_hc = pt6_hc.flatten()

ax6_or=np.mean(u[L_6or,0], axis=0)
by6_or=np.mean(u[L_6or,1], axis=0)
pt6_or = np.array((ax6_or, by6_or))
pt6_or = pt6_or.flatten()
# Euclidean distance
rat9_dist_pt6hcor = np.sqrt(np.sum(np.square(pt6_hc - pt6_or)))

ax6_od=np.mean(u[L_6od,0], axis=0)
by6_od=np.mean(u[L_6od,1], axis=0)
pt6_od = np.array((ax6_od, by6_od))
pt6_od = pt6_od.flatten()
# Euclidean distance
rat9_dist_pt6hcod = np.sqrt(np.sum(np.square(pt6_hc - pt6_od)))

ax6_con=np.mean(u[L_6con,0], axis=0)
by6_con=np.mean(u[L_6con,1], axis=0)
pt6_con = np.array((ax6_con, by6_con))
pt6_con = pt6_con.flatten()
# Euclidean distance
rat9_dist_pt6hccon = np.sqrt(np.sum(np.square(pt6_hc - pt6_con)))





ax7_hc=np.mean(u[L_7hc,0], axis=0)
by7_hc=np.mean(u[L_7hc,1], axis=0)
pt7_hc = np.array((ax7_hc, by7_hc))
pt7_hc = pt7_hc.flatten()

ax7_or=np.mean(u[L_7or,0], axis=0)
by7_or=np.mean(u[L_7or,1], axis=0)
pt7_or = np.array((ax7_or, by7_or))
pt7_or = pt7_or.flatten()
# Euclidean distance
rat9_dist_pt7hcor = np.sqrt(np.sum(np.square(pt7_hc - pt7_or)))

ax7_od=np.mean(u[L_7od,0], axis=0)
by7_od=np.mean(u[L_7od,1], axis=0)
pt7_od = np.array((ax7_od, by7_od))
pt7_od = pt7_od.flatten()
# Euclidean distance
rat9_dist_pt7hcod = np.sqrt(np.sum(np.square(pt7_hc - pt7_od)))

ax7_con=np.mean(u[L_7con,0], axis=0)
by7_con=np.mean(u[L_7con,1], axis=0)
pt7_con = np.array((ax7_con, by7_con))
pt7_con = pt7_con.flatten()
# Euclidean distance
rat9_dist_pt7hccon = np.sqrt(np.sum(np.square(pt7_hc - pt7_con)))





ax8_hc=np.mean(u[L_8hc,0], axis=0)
by8_hc=np.mean(u[L_8hc,1], axis=0)
pt8_hc = np.array((ax8_hc, by8_hc))
pt8_hc = pt8_hc.flatten()

ax8_or=np.mean(u[L_8or,0], axis=0)
by8_or=np.mean(u[L_8or,1], axis=0)
pt8_or = np.array((ax8_or, by8_or))
pt8_or = pt8_or.flatten()
# Euclidean distance
rat9_dist_pt8hcor = np.sqrt(np.sum(np.square(pt8_hc - pt8_or)))

ax8_od=np.mean(u[L_8od,0], axis=0)
by8_od=np.mean(u[L_8od,1], axis=0)
pt8_od = np.array((ax8_od, by8_od))
pt8_od = pt8_od.flatten()
# Euclidean distance
rat9_dist_pt8hcod = np.sqrt(np.sum(np.square(pt8_hc - pt8_od)))

ax8_con=np.mean(u[L_8con,0], axis=0)
by8_con=np.mean(u[L_8con,1], axis=0)
pt8_con = np.array((ax8_con, by8_con))
pt8_con = pt8_con.flatten()
# Euclidean distance
rat9_dist_pt8hccon = np.sqrt(np.sum(np.square(pt8_hc - pt8_con)))



# compute mean for all trials
pre_or_mean = np.nanmean([rat1_dist_prehcor, rat2_dist_prehcor, rat6_dist_prehcor, rat9_dist_prehcor], axis=0)
pre_od_mean = np.nanmean([rat1_dist_prehcod, rat2_dist_prehcod, rat6_dist_prehcod, rat9_dist_prehcod], axis=0)
pre_con_mean = np.nanmean([rat1_dist_prehccon, rat2_dist_prehccon, rat6_dist_prehccon, rat9_dist_prehccon], axis=0)

pt1_or_mean = np.nanmean([rat1_dist_pt1hcor, rat2_dist_pt1hcor, rat6_dist_pt1hcor, rat9_dist_pt1hcor], axis=0)
pt1_od_mean = np.nanmean([rat1_dist_pt1hcod, rat2_dist_pt1hcod, rat6_dist_pt1hcod, rat9_dist_pt1hcod], axis=0)
pt1_con_mean = np.nanmean([rat1_dist_pt1hccon, rat2_dist_pt1hccon, rat6_dist_pt1hccon, rat9_dist_pt1hccon], axis=0)

pt2_or_mean = np.nanmean([rat1_dist_pt2hcor, rat2_dist_pt2hcor, rat6_dist_pt2hcor, rat9_dist_pt2hcor], axis=0)
pt2_od_mean = np.nanmean([rat1_dist_pt2hcod, rat2_dist_pt2hcod, rat6_dist_pt2hcod, rat9_dist_pt2hcod], axis=0)
pt2_con_mean = np.nanmean([rat1_dist_pt2hccon, rat2_dist_pt2hccon, rat6_dist_pt2hccon, rat9_dist_pt2hccon], axis=0)

pt3_or_mean = np.nanmean([rat1_dist_pt3hcor, rat2_dist_pt3hcor, rat6_dist_pt3hcor, rat9_dist_pt3hcor], axis=0)
pt3_od_mean = np.nanmean([rat1_dist_pt3hcod, rat2_dist_pt3hcod, rat6_dist_pt3hcod, rat9_dist_pt3hcod], axis=0)
pt3_con_mean = np.nanmean([rat1_dist_pt3hccon, rat2_dist_pt3hccon, rat6_dist_pt3hccon, rat9_dist_pt3hccon], axis=0)

pt4_or_mean = np.nanmean([rat1_dist_pt4hcor, rat2_dist_pt4hcor, rat6_dist_pt4hcor, rat9_dist_pt4hcor], axis=0)
pt4_od_mean = np.nanmean([rat1_dist_pt4hcod, rat2_dist_pt4hcod, rat6_dist_pt4hcod, rat9_dist_pt4hcod], axis=0)
pt4_con_mean = np.nanmean([rat1_dist_pt4hccon, rat2_dist_pt4hccon, rat6_dist_pt4hccon, rat9_dist_pt4hccon], axis=0)

pt5_or_mean = np.nanmean([rat1_dist_pt5hcor, rat2_dist_pt5hcor, rat6_dist_pt5hcor, rat9_dist_pt5hcor], axis=0)
pt5_od_mean = np.nanmean([rat1_dist_pt5hcod, rat2_dist_pt5hcod, rat6_dist_pt5hcod, rat9_dist_pt5hcod], axis=0)
pt5_con_mean = np.nanmean([rat1_dist_pt5hccon, rat2_dist_pt5hccon, rat6_dist_pt5hccon, rat9_dist_pt5hccon], axis=0)

pt6_or_mean = np.nanmean([rat1_dist_pt6hcor, rat2_dist_pt6hcor, rat6_dist_pt6hcor, rat9_dist_pt6hcor], axis=0)
pt6_od_mean = np.nanmean([rat1_dist_pt6hcod, rat2_dist_pt6hcod, rat6_dist_pt6hcod, rat9_dist_pt6hcod], axis=0)
pt6_con_mean = np.nanmean([rat1_dist_pt6hccon, rat2_dist_pt6hccon, rat6_dist_pt6hccon, rat9_dist_pt6hccon], axis=0)

pt7_or_mean = np.nanmean([rat1_dist_pt7hcor, rat2_dist_pt7hcor, rat6_dist_pt7hcor, rat9_dist_pt7hcor], axis=0)
pt7_od_mean = np.nanmean([rat1_dist_pt7hcod, rat2_dist_pt7hcod, rat6_dist_pt7hcod, rat9_dist_pt7hcod], axis=0)
pt7_con_mean = np.nanmean([rat1_dist_pt7hccon, rat2_dist_pt7hccon, rat6_dist_pt7hccon, rat9_dist_pt7hccon], axis=0)

pt8_or_mean = np.nanmean([rat1_dist_pt8hcor, rat2_dist_pt8hcor, rat6_dist_pt8hcor, rat9_dist_pt8hcor], axis=0)
pt8_od_mean = np.nanmean([rat1_dist_pt8hcod, rat2_dist_pt8hcod, rat6_dist_pt8hcod, rat9_dist_pt8hcod], axis=0)
pt8_con_mean = np.nanmean([rat1_dist_pt8hccon, rat2_dist_pt8hccon, rat6_dist_pt8hccon, rat9_dist_pt8hccon], axis=0)

# Do the same thing for RGS14 with changing Rat strings

plt.ylim([0,2.5])
plt.ylabel("Mean Distance to HC")
                                             
plt.plot(["Pre", "PT1","PT2", "PT3","PT4", "PT5-1","PT5-2", "PT5-3","PT5-4"], [[pre_or_mean],
                                                                               [pt1_or_mean],
                                                                               [pt2_or_mean],
                                                                               [pt3_or_mean],
                                                                               [pt4_or_mean],
                                                                               [pt5_or_mean],
                                                                               [pt6_or_mean],
                                                                               [pt7_or_mean],
                                                                               [pt8_or_mean]], 'go', linestyle="-", markersize=10, label="Mean OR VEH")




plt.plot(["Pre", "PT1","PT2", "PT3","PT4", "PT5-1","PT5-2", "PT5-3","PT5-4"], [[pre_od_mean],
                                                                               [pt1_od_mean],
                                                                               [pt2_od_mean],
                                                                               [pt3_od_mean],
                                                                               [pt4_od_mean],
                                                                               [pt5_od_mean],
                                                                               [pt6_od_mean],
                                                                               [pt7_od_mean],
                                                                               [pt8_od_mean]], 'bo', linestyle="-", markersize=10, label="Mean OD VEH")



plt.plot(["Pre", "PT1","PT2", "PT3","PT4", "PT5-1","PT5-2", "PT5-3","PT5-4"], [[pre_con_mean],
                                                                               [pt1_con_mean],
                                                                               [pt2_con_mean],
                                                                               [pt3_con_mean],
                                                                               [pt4_con_mean],
                                                                               [pt5_con_mean],
                                                                               [pt6_con_mean],
                                                                               [pt7_con_mean],
                                                                               [pt8_con_mean]], 'ko', linestyle="-", markersize=10, label="Mean CON VEH")

plt.legend(loc="upper right")

plt.tight_layout()
plt.show()
