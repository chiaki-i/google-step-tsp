#!/usr/bin/env python3

import sys
import math
import copy
import collections

from adjacent import adjacent_matrix
from common import print_solution, read_input
 
# the cost for one edge = distance between two cities
# with adjacent matrix : O(V^2)

def prim_matrix(adj):
    length = len(adj)
    low = [0] * length
    closest = [0] * length

    for i in range(length):
        low[i] = adj[0][i]

    for i in range(1, length):
        min = low[1]
        current = 1
        for j in range(2, length):
            if min > low[j]:
                min = low[j]
                current = j
        # print(str(current) + ' - ' + str(closest[current]))
        low[current] = math.inf
        for j in range(1, length):
            if low[j] < math.inf and low[j] > adj[current][j]:
                low[j] = adj[current][j]
                closest[j] = current
    return closest

def mst_adjacent_list(closest):
    length = len(closest)
    connected = [] 

    for i in range(length):
        connected.append([closest[i]])
            
    for i in range(length):
        connected[closest[i]].append(i)

    for i in range(2): # to start from vertex 0.
        connected[0].remove(0)
    return connected
    
def rec_simplify(structure, parents):
    if parents:
        first = parents.pop(0)
        target = structure[first]
        parents = parents + target
        for item in target:
            if structure[item]:
                structure[item].remove(first)
            else:
                parents.remove(item)
        if parents:
            rec_simplify(structure, parents)
    return structure
    
# simplify the tree structure
# edges only from parents to children in a tree (no double arrows)
def simplify_structure(connected):
    simple = copy.deepcopy(connected)      
    result = rec_simplify(simple, [0])
    # print('simplified : ')
    # print(result)
    return result

def dfs(graph):
    length = len(graph)
    start = 0
    stack = [start]
    visited = []
    for i in range(length):
        assert stack != []
        current = stack.pop(0)
        if current not in visited:
            visited.append(current)
            stack = graph[current] + stack
    return visited

def bfs(start, goal, graph):
    q = [[start]]                       
    path = []
    while not(len(q) == 0):        
        path = q.pop(0)                 
        current = path[len(path) - 1]
        if current == goal:
            break
        else:
            for x in graph[current]:
                if x not in path:
                    new_path = path[:] 
                    new_path.append(x) 
                    q.append(new_path)
    return path

def directly_connected(city1, city2, graph):
    if city2 in graph[city1]:
        return True
    else:
        return False

def euler_path(connected):
    simple = simplify_structure(connected)
    departing = dfs(simple)
    departing.append(0)
    # print('departing :', departing)
    
    path = []
    for i in range(len(departing) - 1):
        city1 = departing[i]
        city2 = departing[i+1]
        if directly_connected(city1, city2, connected):
            path.append(city1)
        else:
            # print('city1 :', city1, ', city2 :', city2)
            returning = bfs(city1, city2, connected)
            returning = returning[:-1]
            path = path + returning
    path.append(0)
    return path

def reverse_path(connected):
    path = euler_path(connected)
    path.reverse()
    visited = []
    for i in path:
        if i not in visited:
            visited.append(i)
    print(visited)
    return visited

def split_branches(connected): # unused function
    simple = simplify_structure(connected)
    departing = dfs(simple)

    last_node = None
    last_branch = None
    path = []
    while departing:
        branch = []
        while departing:
            city2 = departing[1]
            city1 = departing.pop(0)
            if directly_connected(city1, city2, connected):
                branch.append(city1)
                if len(departing) == 1: # current branch is the last one
                    last_node = departing.pop(0)
                    branch.append(last_node)
            else:
                branch.append(city1)
                remaining_another_branch = departing
                if len(remaining_another_branch) == 1:
                    last_branch = [departing.pop(0)]
                break
        path.append(branch)
    if last_branch is not None:
        path.append(last_branch)
    # print('branches :', path)
    return path

def define_target(euler, connected):
    cnt = collections.Counter(euler)
    lengthy = cnt.most_common()
    result = []
    for item in lengthy:
        if item[1] == 1:
            continue
        else:
            result.append(item[0])
    result.remove(0) # 0 is both start & end. removed later.
    return result

def triangle(city1, city2, city3, adj):
    dist = adj[city1][city2] + adj[city2][city3] - adj[city1][city3]
    return dist

# if there is multiple edges that passes one city, choose the best edge(s) to
# shorten the whole path.
def skip_target(path, target, adj):
    checklist = []
    for i in range(len(path)):
        if path[i] == target:
            diff = triangle(path[i-1], path[i], path[i+1], adj)
            checklist.append((([path[i-1], path[i], path[i+1]], i), diff))
    if len(checklist) < 2:
        assert len(checklist) > 0
        return path
    else:
        dist_difference = 1
        current_place_in_path = 1
        checklist = sorted(checklist, key=lambda x: x[dist_difference])
        checklist.pop(0) # worst edge removed from checklist.
        checklist = sorted(checklist, key=lambda x: x[0][current_place_in_path],
                           reverse=True)
        for i in range(len(checklist)):
            num = checklist[i][0][1] 
            path.pop(num)
    return path

def shortcut(connected, adj):
    euler = euler_path(connected)
    print('before shortcut :', euler)
    targets = define_target(euler, connected)
    print('targets :', targets)
    for target in targets:
        euler = skip_target(euler, target, adj)
    while 0 in euler:
        euler.remove(0)
    euler.append(0) # 0 is the goal.
    print('shortcut :', euler)
    return euler

def two_opt(path, adj):
    length = len(path)
    while True:
        count = 0
        for i in range(length-2):
            city1 = path[i]
            city2 = path[i+1]
            for j in range(i+2, length-1):
                city3 = path[j]
                city4 = path[j+1]
                before = adj[city1][city2] + adj[city3][city4]
                after  = adj[city1][city3] + adj[city2][city4]
                if before > after:
                    new_path = path[i+1:j+1]        
                    path[i+1:j+1] = new_path[::-1]
                    count += 1
        if count == 0:
            break
    return path    

def solve(cities):
    sys.setrecursionlimit(100000) # for "rec_simplify" function in challenge 6.
    adj = adjacent_matrix(cities)
    minimum_spanning_tree = prim_matrix(adj)
    connected = mst_adjacent_list(minimum_spanning_tree)
    path = shortcut(connected, adj)
    solution = two_opt(path, adj)
    return solution

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = solve(read_input(sys.argv[1]))
    print_solution(solution)
