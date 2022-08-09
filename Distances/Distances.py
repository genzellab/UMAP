import os
os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');

import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import umap



sns.set(style='white',context='poster', rc={'figure.figsize':(14,10)} )

# Load whole table and split columns 
myDict = scipy.io.loadmat('Tcell.mat')
T=myDict['Tcell'];


#Rat
rat_np=T[:,1];

#StudyDay
StudyDay_np=T[:,2];

#Trial
trial_np=T[:,3];

#Ripples waveforms
Ripples=T[:,4];


# Flattening

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

# Functions

#Function to compare strings with numpy arrays
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



def sample_ripples(ratString, trialString, dayString):
    M = []

    i = 0
    
    #Rat
    rat=strcmp(rat_np, ratString)
    
    #Trial
    trial = strcmp(trial_np, trialString) & strcmp(StudyDay_np, dayString)
    
    
    logicresult=trial*rat;

    L=binary_feature(Ripples,logicresult)
    
    # check if there is at least 1 True value
    if any(L):
        for i in range(100):
            t=(u[L, :2]);
            np.random.shuffle(t)
            
            K = []
            j=0
            for j in range(50):
                K.append(t[j])
                
                # check the index j+1 is not greater than the number of True values
                if j+1 == L[L==True].shape[0]: 
                    break
            M.append(K)
        
    return M


def compute_centroid_rat(rat_day):
    K = []
    i = 0
    if len(rat_day) > 0:
        for i in range(100):
            a = np.nanmean(rat_day[i], axis=0)
            K.append(a)
        K=np.array(K)    
    return K

def distanceTo_hc(cent_rat_hc, cent_rat_day):
    K = []
    i = 0
    if len(cent_rat_hc) > 0 and len(cent_rat_day) > 0:
            for i in range(100):
                dist_hc = np.sqrt(np.sum(np.square(cent_rat_hc[i,:2] - cent_rat_day[i,:2])))
                K.append(dist_hc)

    return K


def mean_distance(dist_hc_day):
    mean_dist = np.nanmean(dist_hc_day, axis=0)
    
    return mean_dist


Distances=[]
#Rats = ["Rat1","Rat2","Rat6","Rat9","Rat3","Rat4","Rat7","Rat8"]
Trials = ["Presleep", "Post1", "Post2", "Post3", "Post4", "Post5-1", "Post5-2", "Post5-3", "Post5-4"]
Days = ["HC", "OR", "OD", "CON"]

def rat_distances(ratString):
    i = 0
    while (i < len(Trials)):
        trialString = Trials[i]
        j = 0
        K=[]
        while (j < len(Days)):
            if j==0:
                dayString = Days[j]
                sample=sample_ripples(ratString, trialString, dayString)
                centroid_HC=compute_centroid_rat(sample)
            else:
                dayString = Days[j]
                sample=sample_ripples(ratString, trialString, dayString)
                centroid=compute_centroid_rat(sample)
                distance=distanceTo_hc(centroid_HC,centroid)
                day_mean_distance=mean_distance(distance)
                K.append(day_mean_distance)
            j+=1
        Distances.append(K)
        i+=1
        
    return Distances
            
