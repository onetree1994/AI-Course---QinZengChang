import numpy as np
import matplotlib.pyplot as plt

def kmeans(X, k, maxIt):
    '''
    @param X: 数据集
    @param k: 类别数目
    @param maxIt: 最大迭代次数
    '''
    numPoints, numDim = X.shape
    dataSet = np.zeros((numPoints, numDim + 1)) # 额外的一列用来记录类别
    dataSet[:, :-1] = X
    
    centroids = dataSet[np.random.randint(numPoints, size = k)]
    centroids[:, -1] = range(1, k + 1)          # 最后一列是类别的标记
    
    iterations = 0
    oldCentroids = None
    
    while not shouldStop(oldCentroids, centroids, iterations, maxIt): # 函数，多个停止条件，函数返回True则停止
        print("iteration: ", iterations)
#         print("dataSet: \n", dataSet)
#         print("centroids: \n", centroids)
        oldCentroids = np.copy(centroids) # 直接用等号会变成引用
        iterations += 1
        
        # K-means
        updateLabels(dataSet, centroids)
        centroids = getCentroids(dataSet, k)
        
    return dataSet

def shouldStop(oldCentroids, centroids, iterations, maxIt):
    if iterations > maxIt:
        return True
    return np.array_equal(oldCentroids, centroids)
    
def updateLabels(dataSet, centroids):
    numPoints, numDim = dataSet.shape
    for i in range(numPoints):
        label = centroids[0, -1]
#         print(centroids)
#         print(label)
        minDist = np.linalg.norm(dataSet[i, :-1] - centroids[0, :-1])
        for j in range(len(centroids)):
            tempDist = np.linalg.norm(dataSet[i, :-1] - centroids[j, :-1])
#             print(tempDist, minDist)
            if tempDist < minDist:
                minDist = tempDist
                label = centroids[j, -1]
#         print(label)
        dataSet[i, -1] = label
#     print(dataSet)

def getCentroids(dataSet, k):
    result = np.zeros((k, dataSet.shape[1]))
#     print(result)
    for i in range(1, k + 1):
        oneCluster = dataSet[dataSet[:, -1] == i, :-1]
        if oneCluster.shape[0] != 0:
            result[i - 1, :-1] = np.mean(oneCluster, axis = 0)
        result[i - 1, -1] = i
#     print(result)
    return result