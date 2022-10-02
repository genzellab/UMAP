import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cl
from matplotlib import cm
import seaborn as sns
import cv2 as cv2
# import utils.processing_helpers as hproc
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm


sns.set(style='white',context='poster', rc={'figure.figsize':(14,10)} )

def plot_binary(x,y,title:str, xlabel:str = '', ylabel:str='', color = 'r', alpha = 0.1, s = 20):
    '''
        x = u[L,0]
        y = u[L,1]
    '''

    #z=Amp
    #normalize = cl.Normalize(vmin=np.mean(z)-3*np.std(z), vmax=np.mean(z)+3*np.std(z))
    
    #colormap=plt.cm.get_cmap('bwr')
    #colors=colormap(z)
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.01)g
    #sm=plt.scatter(u[:,0],u[:,1],alpha=0.1,s=5,color="b")
    plt.scatter(x,y,alpha=alpha,s=s,color=color)   
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.1,cmap='seismic')
    #plt.hist2d(u[L,0], u[L,1],100)
    #sm=plt.cm.ScalarMappable(cmap=colormap)
    
    #sm.set_clim(vmin=np.min(z),vmax=np.max(z))
    #sm.set_clim(vmin=np.min(z),vmax=220)
    
    #plt.colorbar(sm)
    plt.xlabel(ylabel)
    plt.ylabel(xlabel)
    plt.title(title)
    plt.show()

    #plt.legend(['First line', 'Second line'])

def plot_umap(x,y,z=None, feature = None, title:str = '', is3d = False,figsize=(12, 12), xlabel:str = 'Umap 1', ylabel:str='Umap 2', zlabel:str='Umap 4', cmap='seismic',alpha = 0.6, s = 20):
    ''' 
        x = u[L,0]
        y = u[L,1]
        z = Amp
    '''

    normalize = cl.Normalize(vmin=np.mean(feature)-3*np.std(feature), vmax=np.mean(feature)+3*np.std(feature))
    
    #colormap=plt.cm.get_cmap('bwr')
    #colors=colormap(z)
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.01)g
    fig = plt.figure(figsize=figsize)
    if is3d:
        ax = fig.add_subplot(projection='3d')
        sm=ax.scatter(x, y, z,c=feature,alpha=alpha,s=s,cmap=cmap,norm=normalize)
    else:
        ax = fig.add_subplot()
        sm=plt.scatter(x,y,c=feature,alpha=alpha,s=s,cmap=cmap,norm=normalize)

    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.1,cmap='seismic')
    
    #sm=plt.cm.ScalarMappable(cmap=colormap)
    
    #sm.set_clim(vmin=np.min(z),vmax=np.max(z))
    #sm.set_clim(vmin=np.min(z),vmax=220)
    
    plt.colorbar(sm)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if is3d:
        ax.set_zlabel(zlabel)
    plt.title(title)
    plt.show()


def plot_density(x, y = None,bins = 100, title= 'Figure',window_title='-',xlabel:str = '', ylabel:str='', density=1, figsize=(10,7),vmin=0,vmax=0.2):
    '''
        Either give only x to plot 1-D Density plot
        Or give x and y to plot 2d Density plot
    '''
    #z=Amp
    #normalize = cl.Normalize(vmin=np.mean(z)-3*np.std(z), vmax=np.mean(z)+3*np.std(z))
    
    #colormap=plt.cm.get_cmap('bwr')
    #colors=colormap(z)
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.01)g
    #sm=plt.scatter(u[:,0],u[:,1],alpha=0.1,s=5,color="b")
    #plt.scatter(u[L,0],u[L,1],alpha=0.1,s=20,color="r")   
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.1,cmap='seismic')
    fig, ax = plt.subplots(figsize=figsize)
    fig.canvas.set_window_title(window_title)
    if y is not None:
        plt.hist2d(x, y,100,density=density)
        cmb=plt.colorbar()
        cmb.mappable.set_clim(vmin=0, vmax=0.25)    
    else:
        plt.hist(x,bins,density=density)
    
    cmb.set_label('Density')
    #sm=plt.cm.ScalarMappable(cmap=colormap)
    sm= cm.ScalarMappable()

    #sm.set_clim(vmin=np.min(z),vmax=np.max(z))
    sm.set_clim(vmin=vmin,vmax=vmax)
    ax.set_xlabel(xlabel) 
    ax.set_ylabel(ylabel) 
    #plt.colorbar(sm)
    #plt.xlabel("UMAP1")
    #plt.ylabel("UMAP2")
    plt.title(title)
    
    # show plot
    plt.tight_layout() 
    plt.show()

def bs(A,a,st,ed):
    if st > ed :
        return st
    mid = int((st+ed)//2)
    if A[mid] == a:
        return mid
    if A[mid] > a:
        return bs(A,a,st , mid-1)
    else:
        return bs(A,a,mid+1,ed)

def getIndex(A, a, n):
    return bs(A,a,0,n-1)


def plot3Ddensity(x,y,z, bins = 100, xlabel:str = 'umap 1', ylabel:str='umap 2', zlabel:str = 'umap 4',s=30,linewidths=0.5,cmap='hot',marker='.'):
    ''' 
        Plots 3d histogram for x, y and z
    '''
    X = np.linspace(x.min(), x.max(), num=bins+1)
    Y = np.linspace(y.min(), y.max(), num=bins+1)
    Z = np.linspace(z.min(), z.max(), num=bins+1)
    data = {}
    for xv,yv,zv in zip(x,y,z):
        xi,yi,zi = getIndex(X,xv,bins+1),getIndex(Y,yv,bins+1),getIndex(Z,zv,bins+1)
        xi -= 1
        yi -= 1
        zi -= 1
        if (xi,yi,zi) in data:
            data[(xi,yi,zi)] += 1
        else:
            data[(xi,yi,zi)] = 1
    data = [[k[0], k[1], k[2], v] for k,v in data.items()]
    data = np.array(data)
    # datap = data[:,3]>0.0
    # data = data[datap]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    p3d = ax.scatter(data[:,0], data[:,1], data[:,2], s=s, c=data[:,3].tolist(),linewidths=linewidths,cmap=cmap,marker=marker)
    fig.colorbar(p3d)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.show()


def plotZfeatureOnDensities(x,y, z_feature,bins = 100, plot = True, behaviour = lambda x: x.mean(), xlabel:str = '', ylabel:str='', featureLabel:str = '',s=30,linewidths=0.5,cmap='hot',marker='.'):
    '''
    
        For 2-D density plot of X,Y
        Plot feature Z over the bins
        By default it's mean of all points
        Can change the behaviour 
    
    '''

    X = np.linspace(x.min(), x.max(), num=bins+1)
    Y = np.linspace(y.min(), y.max(), num=bins+1)
    image = np.zeros((bins,bins))
    data = {}
    for xv,yv,zv in zip(x,y,z_feature):
        xi,yi = getIndex(X,xv,bins+1),getIndex(Y,yv,bins+1)
        xi -= 1
        yi -= 1
        if (xi,yi) in data:
            data[(xi,yi)].append(zv)
        else:
            data[(xi,yi)] = [zv]

    data = [[k[0], k[1], v] for k,v in data.items()]
    for item in data:
        res = np.array(item[2])
        item[2] = behaviour(res) if behaviour is not None else res.mean()
        image[item[0]][item[1]] = item[2]

    data = np.array(data)
    # datap = data[:,2]>0.0
    # data = data[datap]
    # data = data[:,2]
    # plt.hist(data, bins=100)
    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(111,)
        p3d = ax.scatter(data[:,0], data[:,1], s=s, c=data[:,2].tolist(),linewidths=linewidths,cmap=cmap,marker=marker)
        cb = fig.colorbar(p3d)
        cb.set_label(featureLabel)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.show()
    return image, X[1:], Y[1:]




def significant_pixels(x,y,z,bins=100, iter=100, pval = 0.5, smooth= False):
    ''' 
        x = u[:,0]
        y = u[:,1]
        z = Meanfreq
        bins = Suggested: 100. It gives a 100x100 density matrix. 
        iter = iterations
        pval = P-value. Suggested: 0.001    
        smooth = True to smooth the image
    '''
    # Determines which pixels have a significant density compared to
    # a permuted control.
    #PARAMETERS:
    #ratString
    #dayString
    #binning: Suggested: 100. It gives a 100x100 density matrix. 
    #p_val: P-value. Suggested: 0.001    
    
    #ratString='Rat1'
    #dayString='CON'
    
    #Rat

    image,_,_=plotZfeatureOnDensities(x,y, z,bins = bins)
    image = (image / image.max())*255

    if smooth:
            image = hproc.smooth_image_custom(image)

    # %% permuting 2D density maps

    L=z
    B=[]
    for i in tqdm(range(iter)):    #Takes several minutes
        # L_permuted=np.random.permutation(L)  # This line
        L_permuted = L.copy()
        np.random.shuffle(L_permuted)
        image_perm,_,_ = plotZfeatureOnDensities(x,y, L_permuted,bins = bins, plot=False)
        if smooth:
            image_perm = hproc.smooth_image_custom(image_perm)
        image_perm=np.ndarray.flatten(image_perm)
        B.append(image_perm)

    B=np.vstack(B)        

    a0=np.ndarray.flatten(image)     

    #p-value calculation (Plusmaze method)   
    D0=[]
    for i in range(a0.size):
        #max(B[:,i])
        distribution=B[:,i]
        #m_d=np.mean(distribution)
        d0=(1+np.sum(distribution >=a0[i]))/(len(distribution)+1) 
        if i==0:
            D0=d0
        else:
            D0=np.vstack((D0,d0))
    # D0 = np.vstack()
               
    D = D0 <= pval         
                        
    D = np.reshape(D,(bins,bins))

    new_image = np.zeros((bins,bins),dtype=np.uint8)
    for xi, xv in enumerate(D == False):
        for yi,yv in enumerate(xv):
            if yv:
                new_image[xi][yi] = image[xi][yi]
    
    return new_image

