# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 15:52:29 2017

@author: OneTree

Generate Gaussian-Mixture distribution dataset, and Swiss-Roll distribution dataset,
 then analyze the performance of K-Means and DBSCAN algorithm toward this two dataset.
"""

import numpy as np
import matplotlib.pyplot as plt
import kmeans as km

from sklearn.cluster import DBSCAN


# generate gaussian distribution data set
gauss1 = np.random.multivariate_normal([1, 1], [[1, 0],[0, 1]], 100)
gauss2 = np.random.multivariate_normal([-4, 0], [[1, 0],[0, 1]], 100)
gauss3 = np.random.multivariate_normal([-5, -5], [[2, 0],[0, 1]], 100)
gauss4 = np.random.multivariate_normal([5, -6], [[1, 0],[-1, 2]], 100)
gauss = np.vstack((gauss1, gauss2, gauss3, gauss4))

# generate swiss-roll-like distribution data set
num = 300
angle = np.random.rand(num)
angle = angle - 0.5
angle = angle*np.pi
r = (np.random.rand(num) - 0.5)*2*0.4 + 2
swissx = np.sin(angle)*r
swissy = np.cos(angle)*r
swiss1 = []
for i in range(0, num):
    swiss1.append([swissx[i], swissy[i]])
angle = np.random.rand(num)
angle = angle - 0.5
angle = angle*np.pi
r = (np.random.rand(num) - 0.5)*2*0.4 + 2
swissx = np.sin(angle+np.pi)*r+2
swissy = np.cos(angle+np.pi)*r
swiss2 = []
for i in range(0, num):
    swiss2.append([swissx[i], swissy[i]])
swiss = np.vstack((swiss1, swiss2))

gauss1 = km.kmeans(gauss, 4, 1000)
swiss1 = km.kmeans(swiss, 2, 1000)

# k-means gauss
unique_labels = set(gauss1[:,-1])
colors = [plt.cm.Spectral(each)
            for each in np.linspace(0, 1, len(unique_labels))]
plt.figure(1)
for k, col in zip(unique_labels, colors):
    class_member_mask = (gauss1[:, -1] == k)
    xy = gauss[class_member_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col))
# k-means swiss
unique_labels = set(swiss1[:,-1])
colors = [plt.cm.Spectral(each)
            for each in np.linspace(0, 1, len(unique_labels))]
plt.figure(2)
for k, col in zip(unique_labels, colors):
    class_member_mask = (swiss1[:, -1] == k)
    xy = swiss[class_member_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col))

gauss2 = DBSCAN(0.5).fit(gauss)
swiss2 = DBSCAN().fit(swiss)

# DBSCAN gauss
unique_labels = set(gauss2.labels_)
colors = [plt.cm.Spectral(each)
            for each in np.linspace(0, 1, len(unique_labels))]
plt.figure(3)
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]
    class_member_mask = (gauss2.labels_ == k)
    xy = gauss[class_member_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col))
# DBSCAN swiss
unique_labels = set(swiss2.labels_)
colors = [plt.cm.Spectral(each)
            for each in np.linspace(0, 1, len(unique_labels))]
plt.figure(4)
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]
    class_member_mask = (swiss2.labels_ == k)
    xy = swiss[class_member_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col))