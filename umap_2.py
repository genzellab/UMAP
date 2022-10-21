
import os
# TODO: Select path wrt your system
# os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');
os.chdir('F:/UMAP/dataset');
# sys.path.append('/home/genzel/Documents/UMAP')

import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
#import plotly.express as px
import utils.plotting_helpers as hplt
import utils.processing_helpers as hproc

sns.set(style='white',context='poster', rc={'figure.figsize':(14,10)} )

# Load data:
data_types = ['all', 'cbd', 'osbasic', 'rgs']
condition = ["CON", "OD", "OR", "HC"]
labels = ['Amplitude', 'Mean Frequency', 'Amplitude 2', 'Mean', 'Frequency', 'Entropy', 'AUC', 'AUC 2']
data_type = data_types[1]

data = hproc.get_data_tcell(f'Tcell_{data_type}.mat')
u = np.load(f'u_{data_type}.npy')

# hplt.plot_umap(u[:,0], u[:,1], u[:,3], feature=data['amp'], title="Amplitude", s=1)
for i, j in zip(range(4), range(1,4)):
    hplt.plot_umap(u[:,i], u[:,j], s=1, xlabel=f'Umap {i}', ylabel = f'Umap {j}')




