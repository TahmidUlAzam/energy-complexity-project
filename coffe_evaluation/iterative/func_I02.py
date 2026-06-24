# COFFE Iterative Example 2
# Source: COFFE function-level benchmark

from operator import itemgetter

def solution(test_list):
    res = min(test_list, key=itemgetter(1))[0]
    return res
