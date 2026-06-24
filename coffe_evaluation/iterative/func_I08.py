# COFFE Iterative Example 8
# Source: COFFE function-level benchmark

def solution(arr):
    MSIBS = arr[:]
    for i in range(len(arr)):
        for j in range(0, i):
            if arr[i] > arr[j] and MSIBS[i] < MSIBS[j] + arr[i]:
                MSIBS[i] = MSIBS[j] + arr[i]
    MSDBS = arr[:]
    for i in range(1, len(arr) + 1):
        for j in range(1, i):
            if arr[-i] > arr[-j] and MSDBS[-i] < MSDBS[-j] + arr[-i]:
                MSDBS[-i] = MSDBS[-j] + arr[-i]
    solution = float('-Inf')
    for (i, j, k) in zip(MSIBS, MSDBS, arr):
        solution = max(solution, i + j - k)
    return solution
