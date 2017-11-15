# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 15:52:29 2017

@author: OneTree

Generate Gaussian-Mixture distribution dataset, and Swiss-Roll distribution dataset,
 then analyze the performance of K-Means and DBSCAN algorithm toward this two dataset.
"""

import numpy as np
import matplotlib.pyplot as plt

# generate gaussian distribution data set
gauss1 = np.random.multivariate_normal([1, 1], [[1, 0],[0, 1]], 100)
gauss2 = np.random.multivariate_normal([-2, 0], [[1, 0],[0, 1]], 100)
gauss3 = np.random.multivariate_normal([-5, -5], [[2, 0],[0, 1]], 100)
gauss4 = np.random.multivariate_normal([5, -6], [[1, 0],[-1, 2]], 100)
gauss = np.vstack((gauss1, gauss2, gauss3, gauss4))

# generate swiss-roll-like distribution data set
num = 300
angle = np.random.rand(num)
angle = angle - 0.5
angle = angle*2/3*np.pi
r = (np.random.rand(num) - 0.5)*2*0.2 + 2
swissx = np.sin(angle)*r
swissy = np.cos(angle)*r
swiss1 = []
for i in range(0, num):
    swiss1.append([swissx[i], swissy[i]])
angle = np.random.rand(num)
angle = angle - 0.5
angle = angle*2/3*np.pi
r = (np.random.rand(num) - 0.5)*2*0.2 + 2
swissx = np.sin(angle+np.pi)*r
swissy = np.cos(angle+np.pi)*r
swiss2 = []
for i in range(0, num):
    swiss2.append([swissx[i], swissy[i]])
swiss = np.vstack((swiss1, swiss2))
for pt in swiss2:
    plt.plot(pt[0], pt[1], 'bo')
# =============================================================================
# for pt in swiss:
#     plt.plot(pt[0], pt[1], 'bo')
# plt.xlim(-10, 10)
# plt.ylim(-10, 10)
# =============================================================================
