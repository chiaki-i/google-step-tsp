#!/usr/bin/env python3

import sys
import math
import copy

from adjacent import adjacent_matrix
from common import read_input
 
# 与えられたグラフが完全グラフだと思えばよい
# グラフのコストとは、ここでは各都市間の距離
# 隣接行列を使った解法の計算量はO(V^2)

def prim_matrix(cities):
    adj = adjacent_matrix(cities)

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
    print('simplified : ', end='')
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

def bfs(start, goal, lst):
    q = [[start]]                       
    answer = []
    path = []
    while not(len(q) == 0):        
        path = q.pop(0)                 
        current = path[len(path) - 1]
        if current == goal:
            break
        else:
            for x in lst[current]:
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
        print('city1 :', city1, ', city2 :', city2)
        if directly_connected(city1, city2, connected):
            path.append(city1)
        else:
            returning = bfs(city1, city2, connected)
            returning = returning[:-1]
            path = path + returning
    return path


if __name__ == '__main__':
    assert len(sys.argv) > 1
    mst = prim_matrix(read_input(sys.argv[1])) # (x座標, y座標)のリスト
    print(mst)
    connected = mst_adjacent_list(mst)
    print('connected :', connected)
    euler = euler_path(connected)
    print('euler :', euler)
    # print_solution(solution)
