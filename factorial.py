# factorial.py - four variants of the factorial algorithm
# (Unoptimised recursion, Memoised recursion, Iterative, Tail recursive) used in this dissertation.
# Variants are imported by run_all_experiments.py for energy measurement.
from functools import lru_cache
from codecarbon import EmissionsTracker
import time

# Variant 1: Unoptimised recursion
# In recursion, a function solves a problem by calling itself on a smaller
# input until it reaches a base case.
# With every recursive call, a new stack frame is added to Python's call stack.
def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)

# Variant 2: Memoised recursion
# Memoisation utilises Python's @lru_cache decorator from the functools
# module and the result of every function call is cached using the @lru_cache decorator.
@lru_cache(maxsize=None)
def factorial_memoized(n):
    if n <= 1:
        return 1
    return n * factorial_memoized(n - 1)

# Variant 3: Iterative
# In iteration, a block or chunk of code is repeated using a for loop or a
# while loop until a specific condition is met. In comparison to recursion,
# no function is called repeatedly in iteration.
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Variant 4: Tail recursive
# Tail recursion is a special kind of recursion that modifies the recursion
# so that the recursive call is performed last by the function.
# Python does not perform TCO so every tail recursive call still builds a new stack
# frame.
def factorial_tail_recursive(n, acc=1):
    if n <= 1:
        return acc
    return factorial_tail_recursive(n - 1, n * acc)

def run_factorial_experiment():
    n = 500  #input size

    tests = [
        ("Iterative",             factorial_iterative),
        ("Memoized",              factorial_memoized),
        ("Tail_Recursive",        factorial_tail_recursive),
        ("Unoptimized_Recursive", factorial_recursive)
    ]

    print(f"--- Starting Factorial Energy Test (n={n}) ---\n")

    for name, func in tests:
        print(f"Running {name}...")

        tracker = EmissionsTracker(
            project_name=f"Factorial_{name}_n{n}",
            measure_power_secs=1,
            save_to_file=True
        )

        # A single Factorial call took microseconds even at large input sizes
        # and this was not reliable for CodeCarbon to measure as it was too short.
        # 5,000 repetitions per trial were used to resolve this.
        REPETITIONS = 5000

        tracker.start()
        start_t = time.time()

        # For the memoised Factorial variant the cache was cleared using
        # cache_clear() before every repetition. This made sure that every
        # repetition started from a cold cache, so the memoisation never
        # actually had the opportunity to be beneficial.
        for _ in range(REPETITIONS):
            if hasattr(func, "cache_clear"):
                func.cache_clear()
            func(n)

        duration = time.time() - start_t
        emissions = tracker.stop()

        print(f"{name} finished in {duration:.4f}s\n")

    print("--- Done! ---")

# Correctness test
# This block runs only when factorial.py is executed directly
# It verifies that all four variants produce the same result for n = 10
# The standalone run_factorial_experiment() function is a development test runner
# the dissertation's main results come from run_all_experiments.py
if __name__ == "__main__":
    n = 10
    print("Recursive:", factorial_recursive(n))
    print("Memoized:", factorial_memoized(n))
    print("Iterative:", factorial_iterative(n))
    print("Tail recursive:", factorial_tail_recursive(n))
    print()


    run_factorial_experiment()