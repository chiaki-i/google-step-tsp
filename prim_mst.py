#!/usr/bin/env python3

import sys
import math

from adjacent import adjacent_matrix
from common import read_input
 
# 与えられたグラフが完全グラフだと思えばよい
# グラフのコストとは、ここでは各都市間の距離

# 優先度付きキュー＋隣接リスト??
# 計算量は O((V+E)logV) = O(ElogV) になるらしい

# 隣接行列を使った解法の計算量はO(V^2)

def prim_matrix(cities):
    adj = adjacent_matrix(cities)

    length = len(cities)
    low_cost = [0] * length
    closest = [0] * length

    for i in range(length):
        low_cost[i] = adj[0][i]

    for i in range(1, length): # 特に i はここでは関与しない
        min = low_cost[1]
        current = 1
        for j in range(2, length):
            if min > low_cost[j]:
                min = low_cost[j]
                current = j
        # print(str(current) + ' - ' + str(closest[current]))
        low_cost[current] = math.inf
        for j in range(1, length):
            if low_cost[j] < math.inf and low_cost[j] > adj[current][j]:
                low_cost[j] = adj[current][j]
                closest[j] = current
    return closest


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    solution = [current_city]

    def distance_from_current_city(to):
        return dist[current_city][to]

    while unvisited_cities:
        next_city = min(unvisited_cities, key=distance_from_current_city)
        unvisited_cities.remove(next_city)
        solution.append(next_city)
        current_city = next_city
        print(solution)
    return solution



if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = prim_matrix(read_input(sys.argv[1])) # (x座標, y座標)のリスト
    print(solution)
    # print_solution(solution)
