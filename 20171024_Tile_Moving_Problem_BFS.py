# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 21:44:23 2017

BFS Search

@author: OneTree
"""
import queue
import copy

# node class
class Node(object):
    def __init__(self, state, blankpos, parent):
        self.state = copy.deepcopy(state)
        self.blankpos = copy.deepcopy(blankpos)
        self.parent = parent
    
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
def isnew(state_node, closed):
    for node in closed:
        if isgoal(node, state_node):
            return False
    return True

# move blank and join new state into open table
def joinopen(state_node, open, closed):
    state = state_node.state
    # up
    blankpos = copy.deepcopy(state_node.blankpos)
    if(blankpos[0] > 0):
        state_child = copy.deepcopy(state)
        temp = state_child[blankpos[0]][blankpos[1]]
        state_child[blankpos[0]][blankpos[1]] = state_child[blankpos[0] - 1][blankpos[1]]
        state_child[blankpos[0] - 1][blankpos[1]] = temp
        blankpos[0] = blankpos[0] - 1
        node_child = Node(state_child, blankpos, state_node)
        if isnew(node_child, closed):
            open.put(node_child)
    # down
    blankpos = copy.deepcopy(state_node.blankpos)
    if(blankpos[0] < 3):
        state_child = copy.deepcopy(state)
        temp = state_child[blankpos[0]][blankpos[1]]
        state_child[blankpos[0]][blankpos[1]] = state_child[blankpos[0] + 1][blankpos[1]]
        state_child[blankpos[0] + 1][blankpos[1]] = temp
        blankpos[0] = blankpos[0] + 1
        node_child = Node(state_child, blankpos, state_node)
        if isnew(node_child, closed):
            open.put(node_child)
    #left
    blankpos = copy.deepcopy(state_node.blankpos)
    if(blankpos[1] > 0):
        state_child = copy.deepcopy(state)
        temp = state_child[blankpos[0]][blankpos[1]]
        state_child[blankpos[0]][blankpos[1]] = state_child[blankpos[0]][blankpos[1] - 1]
        state_child[blankpos[0]][blankpos[1] - 1] = temp
        blankpos[1] = blankpos[1] - 1
        node_child = Node(state_child, blankpos, state_node)
        if isnew(node_child, closed):
            open.put(node_child)
    #right
    blankpos = copy.deepcopy(state_node.blankpos)
    if(blankpos[1] < 3):
        state_child = copy.deepcopy(state)
        temp = state_child[blankpos[0]][blankpos[1]]
        state_child[blankpos[0]][blankpos[1]] = state_child[blankpos[0]][blankpos[1] + 1]
        state_child[blankpos[0]][blankpos[1] + 1] = temp
        blankpos[1] = blankpos[1] + 1
        node_child = Node(state_child, blankpos, state_node)
        if isnew(node_child, closed):
            open.put(node_child)


# start node
state = [[11, 9, 4, 15], [1, 3, 0, 12], [7, 5, 8, 6], [13, 2, 10, 14]]
blankpos = [1, 2]
start = Node(state, blankpos, None)
# goal node
state = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
blankpos = [3, 3]
goal = Node(state, blankpos, None)
# OPEN table
open = queue.Queue()
open.put(start)
# CLOSED table
closed = []

joinopen(start, open, closed)        

# BFS Search
cnt = 0
state = open.get()
while not isgoal(state, goal):
    closed.append(state)
    joinopen(state, open, closed)
#    print(open._qsize())
    state = open.get()
    cnt = cnt + 1;
    if(cnt == 1000):
        cnt = 0
        state.show()