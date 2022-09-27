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

# Computing the clusters/contours. 
```
#ratString
#dayString
# binning=100
# p_val=0.001

p_val=0.001
#Permutation of smoothed density maps.
S1=significant_pixels_smooth(ratString, dayString,binning,p_val);


# Erotion+Dilation
kernel = np.ones((2, 2), np.uint8)
 
# The first parameter is the original image,
# kernel is the matrix with which image is
# convolved and third parameter is the number
# of iterations, which will determine how much
# you want to erode/dilate a given image.
ab = S1.astype(np.uint8)


img_erosion = cv2.erode(ab, kernel, iterations=2)
img_dilation = cv2.dilate(img_erosion, kernel, iterations=3)
```
