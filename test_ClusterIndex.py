#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 12:44:16 2022

@author: adrian
"""
   fig, ax = plt.subplots(figsize =(10, 7))
   
   
   plt.figure(figsize=(10, 6))
   hist1=plt.hist2d(u[L,0], u[L,1],100,density=1,cmap='Reds',alpha=0.6) #OR
   hist2=plt.hist2d(u[M,0], u[M,1],100,density=1,cmap='Blues',alpha=0.6)  #OD
   #HC
   #con
   plt.colorbar(hist1, orientation='vertical')
   plt.colorbar(hist2, orientation='vertical')
   plt.show()
   
   cmb=plt.colorbar()
   cmb.mappable.set_clim(vmin=0, vmax=0.25)    
   cmb.set_label('Density')
   #sm=plt.cm.ScalarMappable(cmap=colormap)
   sm=plt.cm.ScalarMappable()

   #sm.set_clim(vmin=np.min(z),vmax=np.max(z))
   sm.set_clim(vmin=0,vmax=0.2)
   ax.set_xlabel('UMAP1') 
   ax.set_ylabel('UMAP2') 
   #plt.colorbar(sm)
   #plt.xlabel("UMAP1")
   #plt.ylabel("UMAP2")
   plt.title(string)
 
   # show plot
   plt.tight_layout() 
   plt.show()
   
   
   
   import pandas as pd
   df=pd.DataFrame(u, columns=['u1','u2','u3','u4'])
   Meanfreq
   
   
   cI_val, bLab, _=URC_computeClusterIndex_V4.computeClusterIndex_V4(df,Meanfreq,10,['u1','u2'],plotCluster=0,vmin=100, vmax=250)
   
   
   
   
   