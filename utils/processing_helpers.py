import numpy as np
import cv2
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

