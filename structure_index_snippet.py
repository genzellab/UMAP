import pickle
import pandas as pd
import URC_computeClusterIndex_V4
import matplotlib.pyplot as plt
import numpy as np
import os
from multiprocessing import Pool

os.chdir('/home/genzellab/Documents/UMAP/dataset')
# # Getting back the objects:
with open('embeddings.pkl','rb') as f:  # Python 3: open(..., 'rb')
    embeddings= pickle.load(f)    

u_veh_osbasic=embeddings[0];
# u_veh_rgs=embeddings[1];
u_veh_cbd=embeddings[2];
u_cbd_cbd=embeddings[3];
# u_rgs_rgs=embeddings[4];
u_clean=embeddings[5];
u_combined_no_rgs=embeddings[6];


with open('Meanfreq.pkl','rb') as f:  # Python 3: open(..., 'rb')
    Meanfreq_list= pickle.load(f)    

Meanfreq_veh_osbasic_dataset=Meanfreq_list[0];
Meanfreq_veh_cbd_dataset=Meanfreq_list[1];
Meanfreq_cbd_cbd_dataset=Meanfreq_list[2];
Meanfreq_combined=Meanfreq_list[3];
Meanfreq_combined_no_rgs=Meanfreq_list[4];


def structureindex(data):
    (u,feature) = data
    print(u.shape, feature.shape)
    Vmin,Vmax = 100,300
    df = np.array(u)
    feature = np.reshape(feature, (feature.shape[0], 1))    
    cI_val_array_tot=[]
    for _ in range(50):
        cI_val_array=[]
        x = np.random.choice(feature.shape[0], 25_000, replace=False)
        for i in range(4): # 4 dimensions
            for k in range(4):
                if i==k:
                    cI_val=0
                else:
                    tdf, tfeature = df[x], feature[x]
                    tdf = pd.DataFrame(tdf, columns=['u1','u2','u3','u4'])
                    cI_val, bLab, _=URC_computeClusterIndex_V4.computeClusterIndex_V4(tdf,tfeature,10,[tdf.columns[i],tdf.columns[k]],plotCluster=0,vmin=Vmin, vmax=Vmax)
                cI_val_array.append(cI_val)
        cI_val_array_tot.append(cI_val_array)
    cI_val_array= np.array(cI_val_array_tot)
    cI_val_array = np.mean(cI_val_array, axis=0)
    return cI_val_array

def plot_structure_index(cI_val_array, feature_title_string, dataset_str) :
    
    fig,ax = plt.subplots()
    cI_val_array=np.array(cI_val_array)
    cI_val_array.resize(4,4)
    im1 = plt.imshow(cI_val_array, cmap=plt.cm.Greys)
        
    plt.xticks([0,1,2,3], [1,2,3,4])
    plt.yticks([0,1,2,3], [1,2,3,4])
    plt.xlabel('UMAP', loc='center')
    plt.ylabel('UMAP', loc='center')
    plt.title("Structure Index \n ("+ feature_title_string +") dataset: " + dataset_str)
    plt.colorbar()
    plt.savefig(f"{dataset_str}.png")

dataset_str = [
    "VEH OSBasic",
    "VEH CBD",
    "CBD CBD",
    "Combined",
    "Combined no RGS"
]

u = [u_veh_osbasic, u_veh_cbd, u_cbd_cbd,u_clean ,u_combined_no_rgs]
feature = [Meanfreq_veh_osbasic_dataset,Meanfreq_veh_cbd_dataset, Meanfreq_cbd_cbd_dataset, Meanfreq_combined, Meanfreq_combined_no_rgs ]

if __name__ == '__main__':
    with Pool() as p: 
        result = p.map(structureindex, zip (u,feature))
    
    result = np.array(result)
    with open('structure_index_results.npy', "wb") as file:      
        np.save(file, result)
    for res, t in zip(result, dataset_str):
        plot_structure_index(res, "freq",t)
        








