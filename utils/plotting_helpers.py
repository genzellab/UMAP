from array import array
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cl
from matplotlib import cm
import seaborn as sns
import cv2 as cv2
import utils.processing_helpers as hproc
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

def plot_umap(x,y,z=None, feature = None, clipmin=None,clipmax=None, title:str = '', figsize=(12, 12), xlabel:str = 'Umap 1', ylabel:str='Umap 2', zlabel:str='Umap 4', cmap='seismic',alpha = 0.6, s = 20):
    ''' 
        x = u[L,0]
        y = u[L,1]
        z = u[L,3]  if given, will plot a 3d scattter plot
        feature = Amp
        clipmin = plots points with feature value greater than clipmin
        clipmax = plots points with feature value less than clipmax
    '''

    normalize = cl.Normalize(vmin=np.mean(feature)-3*np.std(feature), vmax=np.mean(feature)+3*np.std(feature))
    
    #colormap=plt.cm.get_cmap('bwr')
    #colors=colormap(z)
    #sm=plt.scatter(u[:,0],u[:,1],c=z,alpha=0.6,s=0.01)g
    cmin = np.mean(feature)-3*np.std(feature)
    cmax = np.mean(feature)+3*np.std(feature)

    t = None
    if clipmax is not None or clipmin is not None:
        if clipmax is not None:
            t = feature < clipmax
        if clipmin is not None:
            if t is None:
                t = feature > clipmin
            else:
                t = np.logical_and(t, feature > clipmin)
        x, y, feature = x[t], y[t], feature[t]
        if z is not None:
            z = z[t]
    
    fig = plt.figure(figsize=figsize)
    if z is not None:
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
    plt.clim(cmin,cmax)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if z is not None:
        ax.set_zlabel(zlabel)
    plt.title(title)
    plt.show()
    return t


def plot_density(x, y = None,bins = 100, title= 'Figure',window_title='-', xlabel:str = 'Umap 1', ylabel:str='Umap 2', density=1, figsize=(10,7),vmin=0,vmax=0.2):
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


def plot3Ddensity(x,y,z, bins = 100, xlabel:str = 'umap 1', ylabel:str='umap 2', zlabel:str = 'umap 4',s=30,linewidths=0.5,cmap='hot',marker=None):
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


def plotZfeatureOnDensities(x,y, z_feature,bins = 100, plot = True, behaviour = lambda x, axis: np.mean(x,axis = axis), figsize=(12,12), xlabel:str = 'Umap 1', ylabel:str='Umap 2', featureLabel:str = '',s=30,linewidths=1,cmap='hot',marker=None,indices = False):
    '''
    
        For 2-D density plot of X,Y
        Plot feature Z over the bins
        By default it's mean of all points
        Can change the behaviour 
        eg:
            behaviour = Editor: Line Numbers
        Returns:
            list of 2d arrays of plots for each feature
            1-D array of bins for X and Y
            if indices is true: 
                list of list of indices of datapoints for each bin 
    
    '''
    multiple = z_feature[0] is not int
    if indices:
        sig_indices = {}
    X = np.linspace(x.min(), x.max(), num=bins+1)
    Y = np.linspace(y.min(), y.max(), num=bins+1)

    if multiple :
        m = len(z_feature)
        z_feature = [[*z] for z in zip(*z_feature)]
    else:
        m = 1
        z_feature = [z_feature]
        featureLabel = [featureLabel]

    images = [np.zeros((bins,bins)) for _ in range(m)] 

    data = {}
    for i, (xv,yv) in enumerate(zip(x,y)):
        xi,yi = getIndex(X,xv,bins+1),getIndex(Y,yv,bins+1)
        xi -= 1
        yi -= 1
        if indices :
            if (xi,yi) in sig_indices:
                sig_indices[(xi,yi)].append(i)
            else:
                sig_indices[(xi,yi)] = [i]
     
        if (xi,yi) in data:
           for zi, zv in enumerate(z_feature[i]):
                data[(xi,yi)][zi].append(zv)

        else:
            data[(xi,yi)] = []
            for zv in z_feature[i]:
                data[(xi,yi)].append([zv])


    data = [[k[0], k[1], v] for k,v in data.items()]

    for index,item in enumerate(data):
        res = np.array(item[2])
        res = behaviour(res,axis=1) 
        data[index] = [item[0], item[1],*res]
        

    for i , img  in enumerate(images):
        for d in data:
            img[d[0]][d[1]] = d[2+i]
        images[i] = img


    data = np.array(data)

    # print(data.shape)
    # datap = data[:,2]>0.0
    # data = data[datap]
    # data = data[:,2]
    # plt.hist(data, bins=100)
    if plot:
        for i in range(m):
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111,)
            p3d = ax.scatter(data[:,0], data[:,1], s=s, c=data[:,2+i],linewidths=linewidths,cmap=cmap,marker=marker)
            cb = fig.colorbar(p3d)
            cb.set_label(featureLabel[i])
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            plt.show()
    if indices:
        return images, X[1:], Y[1:], sig_indices 
    else:
        return images, X[1:], Y[1:]




def significant_pixels(x,y,z,bins=100, iter=100, pval = 0.5, smooth= False, plot=True, figsize=(12,12), xlabel:str = 'Umap 1', ylabel:str='Umap 2', featureLabel:str = '',s=30,linewidths=1,cmap='hot',marker=None,pbar=True):
    ''' 
        x = u[:,0]
        y = u[:,1]
        z = Meanfreq
        bins = Suggested: 100. It gives a 100x100 density matrix. 
        iter = iterations
        pval = P-value. Suggested: 0.001    
        smooth = True to smooth the image
        Returns:
            list of 2-d arrays of significant pixels for each feature
            list of indices of significant datapoints for each feature
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


    images, _,  _, indices=plotZfeatureOnDensities(x,y, z,bins = bins, xlabel=xlabel,ylabel=ylabel,featureLabel=featureLabel,s=s,linewidths=linewidths,cmap=cmap,marker=marker,figsize=figsize,indices=True)

    for i,  img in enumerate(images):
        if smooth:
            img = hproc.smooth_image_custom(img)
        images[i] = img.flatten()
        
    # %% permuting 2D density maps
    multiple = z[0] is not int

    if not multiple:
        z = [z]
        featureLabel = [featureLabel]
        

    m = len(images)
    B=[[] for _ in range(m)] 
    
    for _ in tqdm(range(iter)) if pbar else range(iter):    #Takes several minutes
        # L_permuted=np.random.permutation(L)  # This line
        
        features = z
        for i,feature in enumerate(features):
            np.random.shuffle(feature)
            features[i] = feature

        image_perms,_,_ = plotZfeatureOnDensities(x,y, features, bins = bins, plot=False)
        assert(len(features) == len(image_perms))

        for i , imgp in enumerate(image_perms):
            if smooth:
                imgp = hproc.smooth_image_custom(imgp)
            image_perms[i] = imgp.flatten()
        
        for i,_ in enumerate(B):
            B[i].append(image_perms[i])

    for i,b in enumerate(B):
        B[i]=np.vstack(b)        

    for img,b in zip(images, B):
        assert(img.shape[0] == b.shape[1])

    #p-value calculation (Plusmaze method)   
    D=[[] for _ in range(m)] 
    
    for id , (img, b) in enumerate(zip(images,B)):
        
        for i in range(img.size):
            #max(B[:,i])
            distribution = b[:,i]
            #m_d=np.mean(distribution)
            d0=(1+np.sum(distribution >=img[i]))/(len(distribution)+1) 
            if i==0:
                D[id]=d0
            else:
                D[id]=np.vstack((D[id],d0))
        
    
    for i , (d,img) in enumerate(zip(D,images)):
        d = d <= pval   
        d = np.reshape(d, (bins,bins))
        D[i] = d
        img = np.reshape(img,(bins,bins))
        images[i] = img
        
                        

    new_images = []
    significant_indices = [[]] * m
    data = []

    for i,(d, img) in enumerate(zip(D,images)):
        for id, v in np.ndenumerate(d):
            if v:
                try:
                    significant_indices[i].extend(indices[id]) 
                except KeyError:
                    ...
                except IndexError:
                    ... 
        nimg = img * d
        temp = [] 
        for index,v in np.ndenumerate(nimg):
            if v > 0.0:
                temp.append([index[0],index[1],v])
        data.append(np.array(temp))
        new_images.append(nimg)
    

    if plot:
        for d,f in zip(data,featureLabel):
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111,)
            p3d = ax.scatter(d[:,0], d[:,1], s=s, c=d[:,2].tolist(),linewidths=linewidths,cmap=cmap,marker=marker)
            cb = fig.colorbar(p3d)
            cb.set_label(f + ' Significant')
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            plt.show()
    return new_images, significant_indices


def plot_scatter_form_image(img):
    ''' 
    Plots a scatter plot of a 2d matrix 
    '''
    t = []
    for indx , v in np.ndenumerate(img):
        t.append([indx[0], indx[1],v])
    t = np.array(t)
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111,)
    p3d = ax.scatter(t[:,0], t[:,1], c=t[:,2].tolist())
    cb = fig.colorbar(p3d)
    plt.show()