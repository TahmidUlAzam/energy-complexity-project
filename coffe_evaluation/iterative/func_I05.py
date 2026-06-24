# COFFE Iterative Example 5
# Source: COFFE function-level benchmark

import re

def solution(text):
    patterns = '\\w*z.\\w*'
    if re.search(patterns, text):
        return True
    else:
        return False
