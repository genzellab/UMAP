# Compute contours in UMAP embedding.

- Find UMAP contours.

- To compute contours in Matlab use:

```
out = bwperim(im);
imshow(out);
```

- Smooth image.

- Visualize density with 'jet' as Nitzan. 

```
a=plt.hist2d(u[L,0], u[L,1],binning,density=1,cmap='jet',cmin=0, cmax=0.5);
```
