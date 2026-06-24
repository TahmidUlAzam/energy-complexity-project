# COFFE Iterative Example 12
# Source: COFFE function-level benchmark

import heapq

def solution(list1, n):
    largest = heapq.nlargest(n, list1)
    return largest
