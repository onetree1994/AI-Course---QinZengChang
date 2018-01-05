# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 13:26:17 2017

@author: OneTree
"""

# =============================================================================
# Suppose there are N cities in total, and we use a matrix to describe the distance between any 2 cities.
# In order to analyze the performance of our algorithm, we make N a variable, and generate distance matrix
# randomly.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import copy
import time

# class -- TSP
class TSP(object):
    def __init__(self, n = 10, width = 1.0, height = 10.0):
        self.n = n
        self.width = width
        self.height = height
        self.cities = np.zeros([self.n, 2])
        self.matrix = np.zeros([n, n])
        self.distance = 0
        self.route = [];
        for i in range(0, n):
            self.route.append(i)
        
        self.distanceMatrix()
        
    # function -- generate distance matrix of N cities randomly, but to avoid geometry mistake, it is a better
        # way to generate points which represent cities first, then we calculate distances of these points. 
    def distanceMatrix(self):
        cities = np.zeros([self.n, 2])
        for i in range(0, self.n):
            cities[i][0] = np.random.rand()*self.width
            cities[i][1] = np.random.rand()*self.height
        self.cities = cities
        for i in range(0, self.n):
            for j in range(i + 1, self.n):
                distance = np.sqrt(np.square((cities[i][0] - cities[j][0])) + np.square((cities[i][1] - cities[j][1])))
                self.matrix[i][j] = distance
                self.matrix[j][i] = distance
    
    # function -- set new route
    def setRoute(self, route):
        self.route = route
        self.totalDistance()
        
    # function -- calculate total distance
    def totalDistance(self):
        self.distance = 0
        lastCity = self.route[0]
        for i in range(1, self.n):
            self.distance += self.matrix[lastCity, self.route[i]]
            lastCity = self.route[i]
        self.distance += self.matrix[lastCity, self.route[0]]
        
    # function -- draw cities and the route
    def show(self):
        plt.axis([0, self.width, 0, self.height])
        plt.plot(self.cities[:, 0], self.cities[:, 1], 'o')
        routePt = np.zeros([self.n + 1, 2])
        for i in range(0, self.n):
            routePt[i] = self.cities[self.route[i], :]
        routePt[self.n] = routePt[0]
        plt.plot(routePt[:, 0], routePt[:, 1], '-')


# class -- GA
class GA(object):
    def __init__(self, judge, issue, firstLife, lifeCount = 10, crossRate = 0.5, mutateRate = 0.05):
        self.n = len(firstLife)
        self.judge = judge
        self.issue = issue
        self.firstLife = firstLife
        self.lifeCount = lifeCount
        self.crossRate = crossRate
        self.mutateRate = mutateRate
        self.lives = []
        self.initLifes()
        self.fitness = [i for i in range(0, lifeCount)]
        self.totalFitness = 0
   
    # function -- initialize lifes
    def initLifes(self):
        self.lives = []
        for i in range(0, self.lifeCount):
            life = copy.deepcopy(self.firstLife)
            np.random.shuffle(life)
            self.lives.append(life)
        
    # function -- evaluate all lifes
    def evaluate(self):
        self.totalFitness = 0
        for i in range(0, self.lifeCount):
            self.fitness[i] = self.judge(self.issue, self.lives[i], self.n)
            self.totalFitness += self.fitness[i]
            
    # function -- select one life in probability
        # roulette
    def select(self):
        partialSum = 0
        threshold = np.random.uniform(0, self.totalFitness)
        for i in range(0, self.lifeCount):
            partialSum += self.fitness[i]
            if(partialSum >= threshold):
                return self.lives[i]
           
    # function -- cross operator
        # we have avoid repetition
    def cross(self, life1, life2):
        newLife = []
        # 10 times to increase success probability
        for j in range(0, 10):
            lower = np.random.randint(0, self.n - 2)
            upper = np.random.randint(lower + 1, self.n - 1)
            segment1 = life1[lower:upper]
            segment2 = life2[lower:upper]
            # judge if there exists confliction
            conflict_flag = 0
            for i in segment1:
                if i not in segment2:
                    newLife = copy.deepcopy(life1)
                    conflict_flag = 1
            if(conflict_flag == 1):
                continue
            newLife = []
            # if there is not confliction, exchange
            for i in range(0, self.n):
                if(i >= lower and i < upper):
                    newLife.append(life2[i])
                else:
                    newLife.append(life1[i])
            break
        return newLife
    
    # function -- mutate operator
        # exchange to avoid repetition
    def mutate(self, life):
        newLife = copy.deepcopy(life)
        pos1 = np.random.randint(0, self.n - 1)
        pos2 = np.random.randint(0, self.n - 1)       
        temp = newLife[pos1]
        newLife[pos1] = newLife[pos2]
        newLife[pos2] = temp       
        return newLife
    
    # function -- generate next lives
    def newLives(self):
        self.evaluate()
        new_lives = []
        for i in range(0, self.lifeCount):
            crossRandom = np.random.rand()
            mutateRandom = np.random.rand()
            newLife = []
            # cross in probability
            if(crossRandom < self.crossRate):
                newLife = self.cross(self.select(), self.select())
            else:
                newLife = self.select()
            # mutate in probability
            if(mutateRandom < self.mutateRate):
                newLife = self.mutate(newLife)
            new_lives.append(newLife)
        return new_lives
     
    # function -- algorithm control
    def control(self, times):
        for i in range(0, times):
            self.lives = self.newLives()
        best = self.lives[0]
        bestfitness = self.judge(self.issue, best, self.n)
        for i in range(1, self.lifeCount):
            if(self.judge(self.issue, self.lives[i], self.n) > bestfitness):
                best = self.lives[i]
                bestfitness = self.judge(self.issue, best, self.n)
        return best


# class -- GA
class GA2(object):
    def __init__(self, judge, judge2, issue, firstLife, lifeCount = 10, crossRate = 0.5, mutateRate = 0.05):
        self.n = len(firstLife)
        self.judge = judge
        self.judge2 = judge2
        self.issue = issue
        self.firstLife = firstLife
        self.lifeCount = lifeCount
        self.crossRate = crossRate
        self.mutateRate = mutateRate
        self.lives = []
        self.initLifes()
        self.fitness = [i for i in range(0, lifeCount)]
        self.totalFitness = 0
   
    # function -- initialize lifes
    def initLifes(self):
        self.lives = []
        for i in range(0, self.lifeCount):
            life = copy.deepcopy(self.firstLife)
            np.random.shuffle(life)
            self.lives.append(life)
        
    # function -- evaluate all lifes
    def evaluate(self):
        self.totalFitness = 0
        self.fitness = self.judge2(self.issue, self.lives)
        for i in range(0, self.lifeCount):
            self.totalFitness += self.fitness[i]
            
    # function -- select one life in probability
        # roulette
    def select(self):
        partialSum = 0
        threshold = np.random.uniform(0, self.totalFitness)
        for i in range(0, self.lifeCount):
            partialSum += self.fitness[i]
            if(partialSum >= threshold):
                return self.lives[i]
           
    # function -- cross operator
        # we have avoid repetition
    def cross(self, life1, life2):
        newLife = []
        # 10 times to increase success probability
        for j in range(0, 10):
            lower = np.random.randint(0, self.n - 2)
            upper = np.random.randint(lower + 1, self.n - 1)
            segment1 = life1[lower:upper]
            segment2 = life2[lower:upper]
            # judge if there exists confliction
            conflict_flag = 0
            for i in segment1:
                if i not in segment2:
                    newLife = copy.deepcopy(life1)
                    conflict_flag = 1
            if(conflict_flag == 1):
                continue
            newLife = []
            # if there is not confliction, exchange
            for i in range(0, self.n):
                if(i >= lower and i < upper):
                    newLife.append(life2[i])
                else:
                    newLife.append(life1[i])
            break
        return newLife
    
    # function -- mutate operator
        # exchange to avoid repetition
    def mutate(self, life):
        newLife = copy.deepcopy(life)
        pos1 = np.random.randint(0, self.n - 1)
        pos2 = np.random.randint(0, self.n - 1)       
        temp = newLife[pos1]
        newLife[pos1] = newLife[pos2]
        newLife[pos2] = temp       
        return newLife
    
    # function -- generate next lives
    def newLives(self):
        self.evaluate()
        new_lives = []
        for i in range(0, self.lifeCount):
            crossRandom = np.random.rand()
            mutateRandom = np.random.rand()
            newLife = []
            # cross in probability
            if(crossRandom < self.crossRate):
                newLife = self.cross(self.select(), self.select())
            else:
                newLife = self.select()
            # mutate in probability
            if(mutateRandom < self.mutateRate):
                newLife = self.mutate(newLife)
            new_lives.append(newLife)
        return new_lives
     
    # function -- algorithm control
    def control(self, times):
        for i in range(0, times):
            self.lives = self.newLives()
        best = self.lives[0]
        bestfitness = self.judge(self.issue, best, self.n)
        for i in range(1, self.lifeCount):
            if(self.judge(self.issue, self.lives[i], self.n) > bestfitness):
                best = self.lives[i]
                bestfitness = self.judge(self.issue, best, self.n)
        return best
        

# function -- fitness function for TSP
def judge(tsp, route, n):
    tsp.setRoute(route)
    return (n/(20*tsp.distance*(0.01/tsp.width)))**5
# function -- fitness function for TSP
def judge2(tsp, route, n):
    tsp.setRoute(route)
    return (n/(20*tsp.distance*(0.01/tsp.width)))**5
def judge3(tsp, route, n):
    tsp.setRoute(route)
    return 1000/tsp.distance
def judge4(tsp, lives):
    sortArray = []
    for i in range(0, len(lives)):
        tsp.setRoute(lives[i])
        sortArray.append([tsp.distance, i])
    sortArray = sorted(sortArray, reverse=True)
    res = [i for i in range(0, len(lives))]
    for i in range(0, len(lives)):
        res[sortArray[i][1]] = i+1
    return res

N = 200
tsp = TSP(N, 100, 100)
route = tsp.route
ga = GA2(judge3, judge4, tsp, route, 50, 0.9, 0.1)

times = 10000
plt.figure(1)
tsp.setRoute(route)
tsp.show()
performance = np.zeros([times+1, 2])
for i in range(1, times+1):
    route = ga.control(1)
    performance[i] = [i, judge3(tsp, route, N)]
    if(not (i%100)):
        print(judge3(tsp, route, N))
plt.figure(2)
tsp.setRoute(route)
tsp.show()
plt.figure(3)
plt.plot(performance[:,0], performance[:,1], '-')

# algorithm  analysis
# =============================================================================
# N = 20
# tsp = TSP(N, 100, 100)
# firstLife = tsp.route
# 
# plt.figure(1)
# maxtimes = 10000
# route1 = []
# route10 = []
# route100 = []
# route1000 = []
# route10000 = []
# performance = np.zeros([maxtimes, 2])
# 
# start_time = time.time()
# ga = GA(judge, tsp, firstLife, 50, 0.8, 0.1)
# for i in range(1, maxtimes):
#     print(i)
#     route = ga.control(1)
#     if(i == 9):
#         route10 = copy.deepcopy(route)
#     if(i == 99):
#         route100 = copy.deepcopy(route)
#     if(i == 999):
#         route1000 = copy.deepcopy(route)
#     if(i == 9999):
#         route10000 = copy.deepcopy(route)
#     performance[i] = [i, judge(tsp, route, N)]
# end_time = time.time()
# plt.figure(1)
# plt.plot(performance[:,0], performance[:,1], '-')
# plt.figure(2)
# tsp.setRoute(route10000)
# tsp.show()
# =============================================================================
