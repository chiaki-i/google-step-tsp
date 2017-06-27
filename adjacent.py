#!/usr/bin/env python3

import math
import sys
from common import read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# append は遅いらしい
# list.extend(リスト) が比較的早いらしいのでそちらに変更
def adjacent_matrix(cities):
    adjacent = []
    length = len(cities)
    for i in range(length):
        current = []
        for j in range(length):
            if i == j:
                current.append(math.inf)
            else:
                current.append(distance(cities[i], cities[j]))
        adjacent.append(current)
    return adjacent

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = adjacent_matrix(read_input(sys.argv[1])) # (x座標, y座標)のリスト
    print(solution)

'''input_0.csv の場合
[[inf, 1139.468611035281, 679.7227326641358, 829.251122595876, 740.0208580992705], 
[1139.468611035281, inf, 463.63085520669887, 512.7321993957855, 1091.1135139211965], 
[679.7227326641358, 463.63085520669887, inf, 394.51229505232465, 745.9866861116151], 
[829.251122595876, 512.7321993957855, 394.51229505232465, inf, 1124.5662308439055], 
[740.0208580992705, 1091.1135139211965, 745.9866861116151, 1124.5662308439055, inf]]

'''
