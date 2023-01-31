import numpy as np
import cv2
from PIL import Image, ImageFilter
import scipy.io
from sklearn.cluster import DBSCAN


# Data will be a matrix X by 127, where X is the pooled amount of ripples across all trials. 
def v_stack(dur_np):
    DUR=[]

    for i, dur in enumerate(dur_np):
        if not i:
            DUR=dur
        else:
            try:
                DUR=np.vstack((DUR,dur))
            except ValueError:
                ...
    return DUR


#Function to accumulate values from numpy arrays
def h_stack(amplitude_np):    
    Amp=[]
    for i, amp in enumerate(amplitude_np):
        if not i:
            Amp = amp[0]
        else:
            try:
                Amp = np.hstack((Amp, amp[0]))
            except IndexError:
                ...
                
    return Amp        


#Function to compare strings with numpy arrays.
def strcmp(treatment_np,string):       
    return (treatment_np == string)*1


def binary_feature(Ripples,treatment):   
    L=[]

    for i, ripple in enumerate(Ripples):
        v=ripple
        if v.shape[0]:
            L.extend([treatment[i]]*v.shape[0])
    L=np.array(L)
    L=L==1
    return L

def unfold_days2ripples(Ripples,T_column):

    L=[]
    
    for i, ripple in enumerate(Ripples):
        v=ripple;        
        if v.shape[0]:
            L.extend([T_column[i]]*v.shape[0])
    L=np.array(L)
    return L

def smooth_image(ab):
    #ab =np.load(f'{ROOT_DIR}/array_bool2_rat8.npy')
    ab = ab*255
    ab = ab.astype(np.uint8)
    im = Image.fromarray(ab)
    image = im.filter(ImageFilter.GaussianBlur)
    image=np.asarray(image);
    image=image.astype('uint8');

    return image


def smooth_image_custom(ab):
    ab = ab*255
    ab = ab.astype(np.uint8)
    kernel1 = np.array([ [1,3,1],
                        [3,5,3],
                        [1,3,1] ])
    kernel1 = kernel1 / kernel1.sum()
    image = cv2.filter2D(src=ab, ddepth=-1, kernel=kernel1)
    image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel1)    
    image=np.asarray(image);
    image=image.astype('float64');

    return image

def align_data(files, ROOT_DIR = "dataset"):
    metadata = {
        0:[],
        1:[],
        2:[],
        3:[],
        4:[]
    }
    aligned_data = []
    for file in files:
        data = scipy.io.loadmat(f'{ROOT_DIR}/Tcell_{file}.mat')[f'Tcell_{file}']
        labels = extract_labels(data)
        for k, v in labels.items():
            for it in v:
                if it not in metadata[k]:
                    metadata[k].append(it)
        for x in data:
            if x[5].shape[1] != 0:
                sitem = []
                for i, it in enumerate(x):
                    if i == 5:
                        break
                    else:
                        sitem.append(metadata[i].index(it))
                for it in x[5]:
                    item = sitem.copy()
                    item.extend(it)
                    aligned_data.append(item)
    aligned_data = np.array(aligned_data)
    return metadata, aligned_data

def extract_labels (data):
    labels = {
        0:[],
        1:[],
        2:[],
        3:[],
        4:[]
    }
    for x in data:
        labels[0].append(x[0][0])
        labels[1].append(x[1][0])
        labels[2].append(x[2][0])
        labels[3].append(x[3][0])
        labels[4].append(x[4][0])
    labels[0] = set(labels[0])
    labels[1] = set(labels[1])
    labels[2] = set(labels[2])
    labels[3] = set(labels[3])
    labels[4] = set(labels[4])
    return labels


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

def dbscan_outliers(some_embedding, embedding_name,eps_value, min_samples_value,outlier_label):
    #Some embedding: UMAP embedding. Example u_osbasic.
    #embedding_name: String with name. Example "OS basic"
    #eps_value and min_samples_value: Arbitrary arguments for DBSCAN.
    #outlier_label: Label from clustering to be used for identifying outliers.
    
    a=some_embedding[:,0:2]; #First two UMAP components. 
    
    # kmeans = KMeans(n_clusters=4, random_state=0).fit(a)
    # label = kmeans.labels_
    
    clustering = DBSCAN(eps=eps_value, min_samples=min_samples_value).fit(a)
    label=clustering.labels_
    
    
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot()
    p3d =plt.scatter(some_embedding[:,0],some_embedding[:,1],c=label, s=10,cmap='viridis')
    plt.colorbar(p3d)
    ax.set_xlabel('Umap 1')
    ax.set_ylabel('Umap 2')
    plt.title(embedding_name)
    
    outliers_embedding=[label==0];
    outliers_embedding=np.logical_not(outliers_embedding);
    return outliers_embedding
