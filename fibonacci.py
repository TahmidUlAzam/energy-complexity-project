# fibonacci.py - four variants of the Fibonacci algorithm
# (Unoptimised recursion, Memoised recursion, Iterative, Tail recursive) used in this dissertation.
# Variants are imported by run_all_experiments.py for energy measurement.
from codecarbon import EmissionsTracker
from functools import lru_cache
import time


# Variant 1: Unoptimised recursion
# In recursion, a function solves a problem by calling itself on a smaller input
# until it reaches a base case.
# With every recursive call, a new stack frame is added to Python's call stack.
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


# Variant 2: Memoised recursion
# Memoisation utilises Python's @lru_cache decorator from the functools module
# The result of every function call is cached using the @lru_cache decorator.
@lru_cache(maxsize=None)
def fib_memoized(n):
    if n <= 1:
        return n
    return fib_memoized(n - 1) + fib_memoized(n - 2)


# Variant 3: Iterative
# In iteration, a block or chunk of code is repeated using a for loop or a
# while loop until a specific condition is met.
# In comparison to recursion, no function is called repeatedly in iteration.
def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# Variant 4: Tail recursive
# Tail recursion is a special kind of recursion that modifies the recursion
# so that the recursive call is performed last by the function.
# Python does not perform TCO so every tail recursive call still builds a new stack frame.
def fib_tail_recursive(n, a=0, b=1):
    if n == 0: return a
    if n == 1: return b
    return fib_tail_recursive(n - 1, b, a + b)

# Standalone experiment runner used during development
# It is not used to generate the main dissertation results
# The dissertation's results come from run_all_experiments.py
def run_experiment():
    n = 35

    tests = [
        ("Iterative", fib_iterative),
        ("Memoized", fib_memoized),
        ("Tail_Recursive", fib_tail_recursive),
        ("Unoptimized_Recursive", fib_recursive)
    ]

    print(f"--- Starting Energy Dataset Generation (n={n}) --- \n")

    for name, func in tests:
        print(f"Running {name}...")


        tracker = EmissionsTracker(
            project_name=f"Fib_{name}_n{n}",
            measure_power_secs=1,
            save_to_file=True
        )

        tracker.start()
        start_t = time.time()

        func(n)

        duration = time.time() - start_t
        emissions = tracker.stop()

        print(f"{name} finished in {duration:.4f}s. Check CSV for kWh! \n")

    print("--- Done! Your primary dataset is now populated. ---")


# Correctness test
# This block runs only when fibonacci.py is executed directly
# It runs one trial of each variant at n = 35 as a development test
# The standalone run_experiment() function is a development test runner
# the dissertation's main results come from run_all_experiments.py
if __name__ == "__main__":
    run_experiment()