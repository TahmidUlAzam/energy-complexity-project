# COFFE Iterative Example 15
# Source: COFFE function-level benchmark

from itertools import combinations_with_replacement

def solution(l, n):
    return list(combinations_with_replacement(l, n))
