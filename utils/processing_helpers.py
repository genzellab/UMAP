import numpy as np
import cv2
import scipy.io
from PIL import Image, ImageFilter


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