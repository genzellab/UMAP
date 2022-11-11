import numpy as np
import cv2
import scipy.io
from PIL import Image, ImageFilter


# Data will be a matrix X by 127, where X is the pooled amount of ripples across all trials. 
def v_stack(dur_np):
    DUR=[]
    flag = False
    for dur in dur_np:
        try:
            if flag:
                DUR=np.vstack((DUR,dur))
            else:
                DUR = dur
                flag = True
        except ValueError:
            ...
    return DUR


#Function to accumulate values from numpy arrays
def h_stack(amplitude_np):    
    Amp=[]
    flag = False
    for amp in amplitude_np:
        try:
            if flag:
                Amp = np.hstack((Amp, amp[0]))
            else:
                Amp = amp[0]
                flag = True
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


def get_data_tcell(file):
    ''' 
    Returns dictionary containing numpy arrays of:
        Original format:
        'treatment', 'rat', 'studyday', 'trial', 'ripples', 
        
        Vertically stacked: 
        'data'

        Horizontally stacked: 
        'meanfreq', 'amp', 'amp2', 'freq', 'entropy', 'auc', 'auc2'.    
    '''
    my_dict = scipy.io.loadmat(file)
    key = file.split('.')[0]
    keys = ['treatment','rat','studyday', 'trial', 'ripples', 'amp', 'meanfreq', 'amp2', 'freq', 'entropy', 'auc', 'auc2']
    
    T = my_dict[key]
    data = {}
    print(T.shape, T.shape[1])
    for i in range(T.shape[1]):
        if i < 4:
            data[keys[i]] = T[:,i]
        elif i == 4:
            data[keys[i]] = T[:,i]
            data['data'] = v_stack(T[:,i])
        else:
            data[keys[i]] = h_stack(T[:,i])
    
    return data


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


def get_code(metadata, key, value):
    return metadata[key].index(value)


def get_data(data):
    return data[:][5:]

