# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 12:04:56 2017

A* Search

@author: OneTree
"""
import copy
import time
import math

# node class
class Node(object):
    # constructor
    def __init__(self, state, blankpos, parent, step, operate, lost):
        self.state = copy.deepcopy(state)
        self.blankpos = copy.deepcopy(blankpos)
        self.parent = parent
        self.step = step
        self.lastoperate = operate
        self.lost =lost
    
    # function to print this state    
    def show(self):
        for row in self.state:
            for col in row:
                print("%4d" % col, end="" )
            print("\n")
        print("---")
        
# judge if this state is goal
def isgoal(state_node, goal_node):
    state = state_node.state
    goal = goal_node.state
    for i in range(0, 4):
        line = state[i]
        line_goal = goal[i]
        for j in range(0, 4):
            if(line[j] != line_goal[j]):
                return False
    return True

# judge if this state is included in closed table
def isnew(state_node, closed, open):
    for node in closed:
        if isgoal(node, state_node):
            return False
# =============================================================================
#     for node in open:
#         if isgoal(node, state_node):
#             if(node.step > state_node.step):
#                 node.parent = state_node.parent
#                 return False
# =============================================================================
    return True

# evaluation function
def evaluation(node, goal, isshow):
    g = node.step
    f = evaluation2(node.state, g, goal, isshow)
    return f

# evaluation function
def evaluation2(state, g, goal, isshow):
    h = 0
    for i in range(0, 4):
        for j in range(0, 4):
            if(state[i][j] != goal.state[i][j]):
#                h = h + abs(goal.state[i][j] - state[i][j])
                h = h + 1
# =============================================================================
#                 a = abs(goal.state[i][j] % 4 - j)
#                 b = abs(math.floor(goal.state[i][j] / 4.0) - i)
#                 h = h + a + b
# =============================================================================
    f = g + 19 * h
#    f = g + 15 * h
# =============================================================================
#     for i in range(0, 4):
#         for j in range(0, 4):
#             if(state[i][j] != goal.state[i][j]):
#                 h = h + 1
#     f = g + 21 * h
# =============================================================================
    if(isshow):
        print(" g=", g, " h=", h, " f=", f)
    return f


# select best node form OPEN table
def selectnode(open, goal):
    mincost = open[0].lost
    minnode = open[0]
    for i in range(1, len(open)):
        if (open[i].lost < mincost):
            minnode = open[i]
            mincost = open[i].lost
    open.remove(minnode)
    return minnode

# move blank and join new state into open table
def joinopen(state_node, open, closed):
    state = state_node.state
    # up
    if(state_node.step > 500):
        return
    blankpos = copy.deepcopy(state_node.blankpos)
    if(blankpos[0] > 0):
        state_child = copy.deepcopy(state)
        temp = state_child[blankpos[0]][blankpos[1]]
        state_child[blankpos[0]][blankpos[1]] = state_child[blankpos[0] - 1][blankpos[1]]
        state_child[blankpos[0] - 1][blankpos[1]] = temp
        blankpos[0] = blankpos[0] - 1
        node_child = Node(state_child, blankpos, state_node, state_node.step + 1, 0, evaluation2(state_child, state_node.step + 1, goal, False))
        if isnew(node_child, closed, open):
            open.append(node_child)
    # down
    blankpos = copy.deepcopy(state_node.blankpos)
    if(blankpos[0] < 3):
        state_child = copy.deepcopy(state)
        temp = state_child[blankpos[0]][blankpos[1]]
        state_child[blankpos[0]][blankpos[1]] = state_child[blankpos[0] + 1][blankpos[1]]
        state_child[blankpos[0] + 1][blankpos[1]] = temp
        blankpos[0] = blankpos[0] + 1
        node_child = Node(state_child, blankpos, state_node, state_node.step + 1, 1, evaluation2(state_child, state_node.step + 1, goal, False))
        if isnew(node_child, closed, open):
            open.append(node_child)
    #left
    blankpos = copy.deepcopy(state_node.blankpos)
    if(blankpos[1] > 0):
        state_child = copy.deepcopy(state)
        temp = state_child[blankpos[0]][blankpos[1]]
        state_child[blankpos[0]][blankpos[1]] = state_child[blankpos[0]][blankpos[1] - 1]
        state_child[blankpos[0]][blankpos[1] - 1] = temp
        blankpos[1] = blankpos[1] - 1
        node_child = Node(state_child, blankpos, state_node, state_node.step + 1, 2, evaluation2(state_child, state_node.step + 1, goal, False))
        if isnew(node_child, closed, open):
            open.append(node_child)
    #right
    blankpos = copy.deepcopy(state_node.blankpos)
    if(blankpos[1] < 3):
        state_child = copy.deepcopy(state)
        temp = state_child[blankpos[0]][blankpos[1]]
        state_child[blankpos[0]][blankpos[1]] = state_child[blankpos[0]][blankpos[1] + 1]
        state_child[blankpos[0]][blankpos[1] + 1] = temp
        blankpos[1] = blankpos[1] + 1
        node_child = Node(state_child, blankpos, state_node, state_node.step + 1, 3, evaluation2(state_child, state_node.step + 1, goal, False))
        if isnew(node_child, closed, open):
            open.append(node_child)

# goal node
state = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
blankpos = [3, 3]
goal = Node(state, blankpos, None, 0, 0, 0)
# start node
state = [[11, 9, 4, 15], [1, 3, 0, 12], [7, 5, 8, 6], [13, 2, 10, 14]]
blankpos = [1, 2]
start = Node(state, blankpos, None, 0, 0, evaluation2(state, 0, goal, False))
# OPEN table
open = []
open.append(start)
# CLOSED table
closed = []

joinopen(start, open, closed)

# A Star Search
# start timing
starttime = time.clock()
cnt = 0
state = open[0]
while not isgoal(state, goal):
    closed.append(state)
    joinopen(state, open, closed)
    state = selectnode(open, goal)
    cnt = cnt + 1
    if(cnt == 100):
        cnt = 0
        state.show()
        evaluation(state, goal, True)
        print(len(open), len(closed))

# end timing
endtime = time.clock()
print("we find it~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# stack to replay move steps
path = []
tstate = state
path.append(tstate)
while tstate.parent:
    tstate = tstate.parent
    path.append(tstate)

# show result
tstate = path.pop()
tstate.show()
while len(path):
    tstate = path.pop()
    if(tstate.lastoperate == 0):
        print("上")
    elif(tstate.lastoperate == 1):
        print("下")
    elif(tstate.lastoperate == 2):
        print("左")
    elif(tstate.lastoperate == 3):
        print("右")
    tstate.show()
    time.sleep(1)
    
evaluation(state, goal, True)
print("\ntime: ", (endtime - starttime))
