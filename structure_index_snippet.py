import pickle
import pandas as pd
import URC_computeClusterIndex_V4
import matplotlib.pyplot as plt
import numpy as np

# # Getting back the objects:
with open('embeddings.pkl','rb') as f:  # Python 3: open(..., 'rb')
    embeddings= pickle.load(f)    

u_veh_osbasic=embeddings[0];
u_veh_rgs=embeddings[1];
u_veh_cbd=embeddings[2];
u_cbd_cbd=embeddings[3];
u_rgs_rgs=embeddings[4];
u_clean=embeddings[5];
u_combined_no_rgs=embeddings[6];


with open('Meanfreq.pkl','rb') as f:  # Python 3: open(..., 'rb')
    Meanfreq_list= pickle.load(f)    

Meanfreq_veh_osbasic_dataset=Meanfreq_list[0];
Meanfreq_veh_cbd_dataset=Meanfreq_list[1];
Meanfreq_cbd_cbd_dataset=Meanfreq_list[2];
Meanfreq_combined=Meanfreq_list[3];
Meanfreq_combined_no_rgs=Meanfreq_list[4];


def structureindex(u,feature,Vmin,Vmax):
    df=pd.DataFrame(u, columns=['u1','u2','u3','u4'])    
    cI_val_array=[]
    for i in range(4): # 4 dimensions
        for k in range(4):
            if i==k:
                cI_val=0
            else:
                cI_val, bLab, _=URC_computeClusterIndex_V4.computeClusterIndex_V4(df,feature,10,[df.columns[i],df.columns[k]],plotCluster=0,vmin=Vmin, vmax=Vmax)
            cI_val_array.append(cI_val)
    

def plot_structure_index(cI_val_array, feature_title_string) :
    
    fig,ax = plt.subplots()
    cI_val_array=np.array(cI_val_array)
    cI_val_array.resize(4,4)
    im1 = plt.imshow(cI_val_array, cmap=plt.cm.Greys)
        
    plt.xticks([0,1,2,3], [1,2,3,4])
    plt.yticks([0,1,2,3], [1,2,3,4])
    
        
    plt.xlabel('UMAP', loc='center')
    plt.ylabel('UMAP', loc='center')
    plt.title("Structure Index \n ("+ feature_title_string +")")
    
    plt.colorbar()
    
    plt.show()


si_Meanfreq_u_veh_osbasic=structureindex(u_veh_osbasic,Meanfreq_veh_osbasic_dataset,100,300)

plot_structure_index(si_Meanfreq_u_veh_osbasic, "Freq")




