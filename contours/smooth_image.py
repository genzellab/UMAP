#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 17:58:30 2022

@author: adrian
"""
from PIL import Image, ImageFilter
ab =np.load(f'{ROOT_DIR}/array_bool2_rat8.npy')
ab = ab*255
ab = ab.astype(np.uint8)
im = Image.fromarray(ab)
image = im.filter(ImageFilter.GaussianBlur)
plt.imshow(image,cmap='jet')
