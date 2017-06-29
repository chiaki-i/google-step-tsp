#!/usr/bin/env python3

import sys
import math
import copy
import collections

from adjacent import adjacent_matrix, distance
from common import print_solution, read_input
 
# 与えられたグラフが完全グラフだと思えばよい
# グラフのコストとは、ここでは各都市間の距離
# 隣接行列を使った解法の計算量はO(V^2)

def prim_matrix(adj):
    length = len(cities)
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

# 最小木の各頂点と直接連結している点を求める
def mst_adjacent_list(closest):
    length = len(closest)
    connected = [] 

    for i in range(length):
        connected.append([closest[i]])
            
    for i in range(length):
        connected[closest[i]].append(i)

    for i in range(2): # starting from vertex 0.
        connected[0].remove(0)
    return connected

# 奇数次数の頂点のみに関する最大重み完全マッチングを求める
# 各辺の重みを負の数にすれば、最大重み完全マッチングを考えられる
def matching(connected):
    length = len(connected)
    odd = []
    for i in range(length):
        if len(connected[i]) % 2 == 1:
            odd.append((i, connected[i]))
    print(odd) 

    
def rec_simplify(structure, parents):
    if parents: # if not empty
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
# arrows only from parents to children in a tree (no double arrows)
def simplify_structure(connected):
    simple = copy.deepcopy(connected) # copied           
    result = rec_simplify(simple, [0])
    print('simplified : ')
    '''
    for i in range(len(result)):
        print(i, ':', result[i])
    '''
    print(result)
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
    print('departing :', departing)
    
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

def split_branches(connected):
    print('============')
    simple = simplify_structure(connected)
    departing = dfs(simple) # 0 を append してない

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
                if len(departing) == 1: # if the current branch is the last one
                    last_node = departing.pop(0)
                    branch.append(last_node)
            else:
                branch.append(city1)
                if len(departing) == 1: # len(remaining another branch) == 1
                    last_branch = [departing.pop(0)]
                break
        path.append(branch)
    if last_branch is not None:
        path.append(last_branch)
    print('branches :', path)
    
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
    result.remove(0) # 0 はあとで消す
    return result

def between(city1, city2, adj):
    dist = adj[city1][city2]
    return dist

def skip_target(path, target, adj):
    checklist = []
    for i in range(len(path)):
        if path[i] == target:
            dist = between(path[i-1], path[i+1], adj)
            checklist.append((([path[i-1], path[i], path[i+1]], i), dist))
    print('checklist for', target, checklist)
    if len(checklist) < 2:
        assert len(checklist) > 0
        return path
    else:
        checklist = sorted(checklist, key=lambda x: x[1]) # 距離の小さい順
        checklist.pop(0)
        print('sorted :', checklist)
        print()
        # 後ろからpopしたい
        checklist = sorted(checklist, key=lambda x: x[0][1], reverse=True)
        for i in range(len(checklist)):
            num = checklist[i][0][1] 
            print(num)
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
    euler.append(0)
    print('shortcut :', euler)
    return euler

if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    adj = adjacent_matrix(cities)
    mst = prim_matrix(adj)
    connected = mst_adjacent_list(mst)
    print('connected :', connected)
    euler = euler_path(connected)
    print('euler :', euler)

    # input 1
    path = reverse_path(connected)

    split_branches(connected)

    solution = shortcut(connected, adj)
    print_solution(solution)
    # print_solution(euler)
