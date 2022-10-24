
import os
# TODO: Select path wrt your system
# os.chdir('/mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP');
os.chdir('F:/UMAP/dataset');
# sys.path.append('/home/genzel/Documents/UMAP')

import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
from sklearn.cluster import DBSCAN, OPTICS, KMeans
#import plotly.express as px
import utils.plotting_helpers as hplt
import utils.processing_helpers as hproc

sns.set(style='white',context='poster', rc={'figure.figsize':(14,10)} )

# Load data:
data_type_index = 1
feature_index = 1

data_types = ['all', 'cbd', 'OSBASIC', 'RGS14']
condition = ["CON", "OD", "OR", "HC"]
labels = ['Amplitude', 'Mean Frequency', 'Amplitude 2', 'Mean', 'Frequency', 'Entropy', 'AUC', 'AUC 2']

data_type = data_types[data_type_index]

# data = hproc.get_data_tcell(f'Tcell_{data_type}.mat')
u = np.load(f'u_{data_type}.npy')

print(u.shape)


# hplt.plot_umap(u[:,0], u[:,1], u[:,3], feature=data['amp'], title="Amplitude", s=1)
# for i, j in zip(range(4), range(1,4)):
#     hplt.plot_umap(u[:,i], u[:,j], s=1, xlabel=f'Umap {i+1}', ylabel = f'Umap {j+1}')



L, data = hplt.plot2Ddensity(u[:,0], u[:,1], plot = False)

label = np.zeros(u[:,0].shape)
for i, l in enumerate(u[:,0]):
    label[i] = data[L[(u[i,0], u[i,1])]]

# X = np.array([ [l] for l in label ])
X = np.array([ [l[0], l[1]] for l in u ])
min_samples = 100
max_eps = 5
# clustering = OPTICS(max_eps=max_eps, min_samples=min_samples).fit_predict(X)
kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
label = kmeans.labels_ 

fig = plt.figure()
ax = fig.add_subplot(111)
p3d = ax.scatter(u[:,0], u[:,1], c=label, s=1)  
ax.set_xlabel('Umap 1', fontsize=14)
ax.set_ylabel('Umap 2',fontsize=14)
# ax.set_title(f'Data :- {data_type}, min_samples:- {min_samples} max_eps:- {max_eps}\nClusters of umap1 and umap2', fontsize=16)
ax.set_title(f'Data :- {data_type}, min_samples:- {min_samples} max_eps:- {max_eps}\nClusters of density of umap1 and umap2 with 100 bins', fontsize=16)
fig.colorbar(p3d)
plt.show()

cl = label == 4             # the binary vector for the rightmost cluster for CBD
fig = plt.figure()
ax = fig.add_subplot(111)
d1, d2 = u[cl], u[cl != True] 
ax.scatter(d2[:,0], d2[:,1], c='grey', alpha=0.4,s=1)
ax.scatter(d1[:,0], d1[:,1], c='red', alpha=0.7,s=1)
ax.set_xlabel('Umap 1', fontsize=14)
ax.set_ylabel('Umap 2',fontsize=14)

plt.show()

data_type_index = 2         # osbasic
data_type = data_types[data_type_index]

# data = hproc.get_data_tcell(f'Tcell_{data_type}.mat')
u = np.load(f'u_{data_type}.npy')


cl = u[:,0] > 1.99             # the binary vector for the rightmost cluster for OSBASIC
fig = plt.figure()
ax = fig.add_subplot(111)
d1, d2 = u[cl], u[cl != True] 
ax.scatter(d2[:,0], d2[:,1], c='grey', alpha=0.4,s=1)
ax.scatter(d1[:,0], d1[:,1], c='red', alpha=0.7,s=1)
ax.set_xlabel('Umap 1', fontsize=14)
ax.set_ylabel('Umap 2',fontsize=14)

plt.show()
