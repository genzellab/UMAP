#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 17:55:45 2022

@author: adrian
"""
ab =np.load(f'{ROOT_DIR}/array_bool2_rat8.npy')
ab = ab*255
ab = ab.astype(np.uint8)
imgray = ab.copy()
ret, thresh = cv2.threshold(imgray, 254, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
c = cv2.drawContours(np.dstack([imgray,imgray,imgray]), contours, -1, (255,0,0), 3)
plt.imshow(c)