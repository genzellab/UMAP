# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:05:59 2023

@author: Linzan Liu
"""



import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from persim import plot_diagrams
from persim import persistent_entropy
import ripser
import random
import gc

os.chdir('/scratch/genzel')
# # Getting back the objects:
with open('Data.pkl','rb') as f:  # Python 3: open(..., 'rb')
    Data= pickle.load(f)    



Data_veh_osbasic_dataset = np.array(Data[0])
Data_veh_cbd_dataset = np.array(Data[2])
Data_cbd_cbd_dataset = np.array(Data[3])
Data_combined_no_rgs = np.array(Data[6])

def plot_persistence_diagrams(X,dataset_name):
      
        
        #bootstrap_samples = np.random.choice(X.shape[0], 30_000, replace=True)
        
        diagrams = ripser.ripser(X, maxdim=2, thresh=17, n_perm=3000)
        Barcodes = diagrams['dgms']
        
        
        #Plot the barcode for H0
        fig, ax = plt.subplots()
        for i in range(len(Barcodes[0])):
            if Barcodes[0][i][1] < np.inf:
                ax.plot([Barcodes[0][i][0], Barcodes[0][i][1]], [i, i], 'b')
        plt.xlim(0,20)
        plt.ylim(0,None)
        ax.set_title('Persistence Barcode (H0)')
        ax.set_xlabel('Filtration Value')
        ax.set_ylabel('Homology Generator')
        fig.savefig(f'{dataset_name}_H0.pdf')
	
        
        #Plot the barcode for H1
        fig, ax = plt.subplots()
        for i in range(len(Barcodes[1])):
            if Barcodes[1][i][1] < np.inf:
                ax.plot([Barcodes[1][i][0], Barcodes[1][i][1]], [i, i], 'r')
        plt.xlim(0,20)
        plt.ylim(0,None)
        ax.set_title('Persistence Barcode (H1)')
        ax.set_xlabel('Filtration Value')
        ax.set_ylabel('Homology Generator')
        fig.savefig(f'{dataset_name}_H1.pdf')
        
         #Plot the barcode for H2
        fig, ax = plt.subplots()
        for i in range(len(Barcodes[2])):
            if Barcodes[2][i][1] < np.inf:
                ax.plot([Barcodes[2][i][0], Barcodes[2][i][1]], [i, i], 'g')
        plt.xlim(0,20)
        plt.ylim(0,None)
        ax.set_title('Persistence Barcode (H2)')
        ax.set_xlabel('Filtration Value')
        ax.set_ylabel('Homology Generator')
        fig.savefig(f'{dataset_name}_H2.pdf')
        

datasets = [Data_veh_osbasic_dataset,Data_veh_cbd_dataset, Data_cbd_cbd_dataset, Data_combined_no_rgs]
if __name__ == '__main__':
    for dataset_name, dataset in [('Data_veh_osbasic_dataset', Data_veh_osbasic_dataset),
                                  ('Data_veh_cbd_dataset', Data_veh_cbd_dataset),
                                  ('Data_cbd_cbd_dataset', Data_cbd_cbd_dataset),
                                  ('Data_combined_no_rgs', Data_combined_no_rgs)]:
        X = np.array(dataset)
        plot_persistence_diagrams(X, dataset_name)
        del X
        gc.collect()

