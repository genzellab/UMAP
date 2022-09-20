Dependencies: To-add. 


# UMAP
Repository for UMAP project. 

## Main folders: :file_folder: 

*Matlab scripts:*
* downsample : Downsampling of HPC and PFC signals to 2500 Hz. 
* detection : Detection of ripple events. 
* preprocessing: Ripple extraction, alignment, filtering, normalization and organization in a table. 

*Python scripts:*

For the following steps, one needs to switch to python. Create a umap environment using the [environment.yml](https://github.com/genzellab/UMAP/blob/main/environment.yml) file.


# UMAP functions

•	flatcells: Function to accumulate values from Numpy array. It iterates across trials , extracts features of events and stacks them together. 

•	strcmp: Function to compare strings with numpy arrays. Output is a binary vector with 1 if the string matches. 

•	binary_feature: Returns a vector with True or False values indicating if a ripple meets some criteria. Usually used after strcmp.

•	plot_umap: Plots the UMAP embedding including the labels of a specific feature. 

•	plot_binary: Takes as an input a binary vector indicating if the ripples meet some criteria. For example, do the ripples belong to Rat 9? The output is a density plot in the UMAP embedding. 

