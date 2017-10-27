# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:46:49 2017

Gomoku Alpha-Beta Pruning

@author: OneTree
"""
import copy
import os
# Node class
class Node(object):
    # constructor
    def __init__(self, state, parent, step):
        self.state = copy.deepcopy(state)
        self.parent = copy.deepcopy(parent)
        self.parent = copy.deepcopy(step)
    
    # function to print this state    
    def show(self):
        for row in self.state:
            for col in row:
                if(col == 1):
                    print("%4c" % "◉", end="" )
                elif(col == 2):
                    print("%4c" % "○", end="" )
                else:
                    print("%4c" % " ", end="" )
            print("\n")
        print("---")


# evaluate this position of one player
def evaluation(state, pos, player):
# =============================================================================
#         we have to consider a series of factors on 4 lines centered of this position.
#         1. on one line, every self-pieces brings positive value, every empty-pieces brings positive value too. 
#         2. on one line, every enemy-pieces brings negative value
#         3. on one line, if 2 enemy-pieces are on different side, then this line is unvaluable.
# =============================================================================
    selfv = 5
    emptyv = 2
    enemyv = -10
    continuity_step = 2
    v1, v2, v3, v4 = 0, 0, 0, 0
    intrv1, intrv2, intrv3, intrv4 = -1, -1, -1, -1
    # 0 degree
    continuity = 1
    k = pos[0] - max(0, pos[0] - 4)
    for i in range(1,k+1):
        # print(v1)
        if(state[pos[0] - i][pos[1]] == player):
            v1 = v1 + selfv ** continuity
            continuity = continuity * continuity_step
        elif(state[pos[0] - i][pos[1]] == 0):
            v1 = v1 + emptyv ** continuity
        else:
            v1 = v1 + enemyv
            intrv1 = i
            break
    k = min(14, pos[0] + 4) - pos[0]
    for i in range(1, k+1):
        if(state[pos[0] + i][pos[1]] == player):
            v1 = v1 + selfv ** continuity
            continuity = continuity * continuity_step
        elif(state[pos[0] + i][pos[1]] == 0):
            v1 = v1 + emptyv ** continuity
        else:
            # space in 2 enemy-pieces cannot not contain 5 self-peices
            v1 = v1 + enemyv
            if(intrv1 != -1):
                if((i - intrv1) <= 5):
                    v1 = 0
            break
    # 45 degree
    continuity = 1
    k = 4
    if((pos[0] - 4) < 0):
        k = pos[0]
    if((pos[1] + 4) >= 15 & (15 - pos[1]  - 1) < k):
        k = 15 - pos[1] - 1
    for i in range(1, k + 1):
        if(state[pos[0] -  i][pos[1] + i] == player):
            v2 = v2 + selfv ** continuity
            continuity = continuity * continuity_step
        elif(state[pos[0] -  i][pos[1] + i] == 0):
            v2 = v2 + emptyv ** continuity
        else:
            v2 = v2 + enemyv
            if(intrv2 == -1):
                intrv2 = pos[0] -  i
            break
    k = 4
    if((pos[1] - 4) < 0):
        k = pos[1]
    if((pos[0] + 4) >= 15 & (15 - pos[0] - 1) < k):
        k = 15 - pos[0] - 1
    for i in range(1, k + 1):
        if(state[pos[0] +  i][pos[1] - i] == player):
            v2 = v2 + selfv ** continuity
            continuity = continuity * continuity_step
        elif(state[pos[0] +  i][pos[1] - i] == 0):
            v2 = v2 + emptyv ** continuity
        else:
            v2 = v2 + enemyv
            # space in 2 enemy-pieces cannot not contain 5 self-peices
            if(intrv2 != -1):
                if((pos[0] + i - intrv2) <= 5):
                    v2 = 0
            break
    # 90 degree
    continuity = 1
    k = pos[1] - max(0, pos[1] - 4)
    for i in range(1, k + 1):
        if(state[pos[0]][pos[1] - i] == player):
            v3 = v3 + selfv ** continuity
            continuity = continuity * continuity_step
        elif(state[pos[0]][pos[1] - i] == 0):
            v3 = v3 + emptyv ** continuity
        else:
            v3 = v3 + enemyv
            intrv1 = i
            break
    # continuity = 1
    k = min(14, pos[1] + 4) - pos[1]
    for i in range(1, k + 1):
        if(state[pos[0]][pos[1] + i] == player):
            v3 = v3 + selfv ** continuity
            continuity = continuity * continuity_step
        elif(state[pos[0]][pos[1]+i] == 0):
            v3 = v3 + emptyv ** continuity
        else:
            v3 = v3 + enemyv
            # space in 2 enemy-pieces cannot not contain 5 self-peices
            if(intrv3 != -1):
                if((i - intrv3) <= 5):
                    v3 = 0
            break
        
    # 135 degree
    k = 4
    continuity = 1
    if((pos[0] - 4) < 0):
        k = pos[0]
    if((pos[1] - 4) < 0 & (pos[1]) < k):
        k = pos[1]
    for i in range(1, k + 1):
        if(state[pos[0] -  i][pos[1] - i] == player):
            v4 = v4 + selfv ** continuity
            continuity = continuity * continuity_step
        elif(state[pos[0] -  i][pos[1] - i] == 0):
            v4 = v4 + emptyv ** continuity
        else:
            v4 = v4 + enemyv
            if(intrv4 == -1):
                intrv4 = pos[0] -  i
            break
    k = 4
    if((pos[0] + 4) >= 15):
        k = 15 - pos[0] - 1
    if((pos[1] + 4) >= 15 & (15 - pos[1] - 1) < k):
        k = 15 - pos[1] - 1
    for i in range(1, k + 1):
        if(state[pos[0] +  i][pos[1] + i] == player):
            v4 = v4 + selfv ** continuity
            continuity = continuity * continuity_step
        elif(state[pos[0] +  i][pos[1] + i] == 0):
            v4 = v4 + emptyv ** continuity
        else:
            v4 = v4 + enemyv
            # space in 2 enemy-pieces cannot not contain 5 self-peices
            if(intrv4 != -1):
                if((pos[0] + i - intrv4) <= 5):
                    v4 = 0
            break
#    print(v1, v2, v3, v4)
    return (v1+v2+v3+v4)

# maxvaluepos
def maxvaluepos(state, player):
    value = 0
    tempos = [0, 0]
    for k1 in range(0, 15):
        for k2 in range(0, 15):
            if(state[k1][k2] == 0):
                tvalue = evaluation(state, [k1, k2], player)
                if(tvalue > value):
                    value = tvalue
                    tempos = [k1, k2]
    return tempos

# maxvaluepos
def maxvaluepos2(state, player, emyv, minvalue):
    value = 0
    tempos = [0, 0]
    for k1 in range(0, 15):
        for k2 in range(0, 15):
            if(state[k1][k2] == 0):
                tvalue = evaluation(state, [k1, k2], player)
                tvalue = tvalue
                if(tvalue > value):
                    # pruning
                    if((emyv - tvalue) < minvalue):
                        return None;
                    value = tvalue
                    tempos = [k1, k2]
    return tempos

# alpha-beta
def game(state, player):
    value = -100000
    pos = [0, 0]
    empos = [0, 0]
    for i in range(0, 15):
        for j in range(0, 15):
            if(state[i][j] == 0):
                curvalue = evaluation(state, [i, j], player)
                tvalue = 0
                tstate = copy.deepcopy(state)
                tstate[i][j] = player
                tempos = [0, 0]
                if(player == 1):
                    #tempos = maxvaluepos(tstate, 2)
                    tempos = maxvaluepos2(tstate, 2, curvalue, value)
                    if(tempos == None):
                        continue
                    tvalue = evaluation(tstate, tempos, 2)
                else:
                    #tempos = maxvaluepos(tstate, 1)
                    tempos = maxvaluepos2(tstate, 1, curvalue, value)
                    if(tempos == None):
                        continue
                    tvalue = evaluation(tstate, tempos, 1)
# =============================================================================
#                 for k1 in range(0, 15):
#                     for k2 in range(0, 15):
#                         if(tstate[k1][k2] == 0):
#                             if(player == 1):
#                                 ktvalue = evaluation(tstate, [k1, k2], 2)
#                             else:
#                                 ktvalue = evaluation(tstate, [k1, k2], 1)
#                             if(ktvalue > tvalue):
#                                 tvalue = ktvalue
#                                 tempos = [k1, k2]
# =============================================================================
                # alpha-beta process
# =============================================================================
#                 if(player == 1):
#                     tempos = maxvaluepos(tstate, 2, empos, evaluation(state, [i, j], player), value)
#                 else:
#                     tempos = maxvaluepos(tstate, 1, empos, evaluation(state, [i, j], player), value)
#                 if(player == 1):
#                     tvalue =  evaluation(state, tempos, 2)
#                 else:
#                     tvalue =  evaluation(state, tempos, 1)
# =============================================================================
                
                tvalue = curvalue - tvalue
                if(tvalue > value):
                    empos = copy.deepcopy(tempos)
                    value = tvalue
                    pos = [i, j]
            
    print(pos, empos)                           
    state[pos[0]][pos[1]] = player

# judge if win
def iswin(state, player):
    return 0
        
# initialize state    
line = []
state = []
for i in range(0, 15):
    line.append(0)
for i in range(0, 15):
    state.append(copy.deepcopy(line))
# start Node
state[6][6], state[6][7], state[6][8], state[7][7], state[8][6], state[8][7], state[8][8], state[9][6], state[10][5], state[10][6], state[10][7] = 1,1,1,1,1,1,1,1,1,1,1 
state[7][5], state[7][6], state[7][8], state[8][5], state[8][9], state[9][5], state[9][7], state[9][9], state[10][4], state[11][6] = 2,2,2,2,2,2,2,2,2,2

start = Node(state, None, 0)
start.show()

#game(start.state, 1)
#start.show()
#print(maxvaluepos(state, 1))
#print(maxvaluepos(state, 2))
#print(evaluation(start.state, [6, 5], 2))
#print(evaluation(start.state, [6, 9], 2))


while 1:
    game(start.state, 2)
    start.show()
    os.system("pause")
    game(start.state, 1)
    start.show()
    os.system("pause")
    
# =============================================================================
# In the evaluation section, I included some acceptable factors, all these factors just effect in 4 valuable directions around the point we analyze.
# 1.	Every self-pieces brings positive score.
# 2.	Every enemy-pieces brings negative score.
# 3.	Every continuous self-pieces pattern brings more score, and the additional score is an exponent of continuous pieces number.
# Actually, the most difficult thing is these parameters, I have to try a lot to make clear which group is more effective.
# 
# =============================================================================
