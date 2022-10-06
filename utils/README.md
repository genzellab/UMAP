# Plotting helpers function description

•	_plot_umap_: Plots the UMAP embedding including the labels of a specific feature. One can select ranges of features. Example: Frequencies between 120 and 160 Hz. It will also output a binary vector ‘t’ which will indicate which ripples meet the specified range. If neither a lower or upper bound range are selected t remains void. 

•	_plot_umap_binary_: Plots overlap of ripples selected based on ranges. 

•	_plot_density_ (formerly plot_binary) Takes as an input a binary vector indicating if the ripples meet some criteria. For example, do the ripples belong to Rat 9? The output is a density plot in the UMAP embedding. 

•	_significant_pixels_: list of 2-d arrays of significant pixels for each feature. list of indices of significant datapoints for each feature
