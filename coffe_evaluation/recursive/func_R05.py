# COFFE Recursive Example 5
# Source: COFFE function-level benchmark

def solution(n, m):
    if m >= n or n == 0:
        return 0
    if m == 0:
        return 1
    return (n - m) * solution(n - 1, m - 1) + (m + 1) * solution(n - 1, m)
