# hanoi.py - two variants of the Towers of Hanoi algorithm
# (Recursive, Iterative) used in this dissertation.
# Variants are imported by run_all_experiments.py for energy measurement.
from codecarbon import EmissionsTracker
import time

# Variant 1: Recursive
# In recursion, a function solves a problem by calling itself on a smaller
# input until it reaches a base case.
# With every recursive call, a new stack frame is added to Python's call stack.
def hanoi_recursive(n, source, target, helper):
    if n == 0:
        return
    hanoi_recursive(n - 1, source, helper, target)
    hanoi_recursive(n - 1, helper, target, source)


# Variant 2: Iterative
# The iterative variant of Towers of Hanoi is a special case.
# The algorithm cannot be written as a simple loop as it is naturally recursive.
# The iterative variant simulates recursion manually by using Python list as a
# stack using .append() and .pop() to push and pop items.
def hanoi_iterative(n, source, target, helper):
    stack = [(n, source, target, helper, False)]
    while stack:
        n, s, t, h, visited = stack.pop()
        if n == 0:
            continue
        if visited:
            stack.append((n - 1, h, t, s, False))
        else:
            stack.append((n, s, t, h, True))
            stack.append((n - 1, s, h, t, False))

# Standalone experiment runner used during development
# It is not used to generate the main dissertation results
# The dissertation's results come from run_all_experiments.py
def run_hanoi_experiment():
    n = 20  # ~1 million moves for measurable runtime

    tests = [
        ("Recursive", hanoi_recursive),
        ("Iterative", hanoi_iterative)
    ]

    print(f"--- Starting Hanoi Energy Test (n={n}) ---\n")

    for name, func in tests:
        print(f"Running {name}...")

        tracker = EmissionsTracker(
            project_name=f"Hanoi_{name}_n{n}",
            measure_power_secs=1,
            save_to_file=True
        )

        REPETITIONS = 10

        tracker.start()
        start_t = time.time()

        for _ in range(REPETITIONS):
            func(n, "A", "C", "B")

        duration = time.time() - start_t
        emissions = tracker.stop()

        print(f"{name} finished in {duration:.4f}s\n")

    print("--- Done! ---")


# Correctness test
# This block runs only when hanoi.py is executed directly
# It runs each variant once at n = 5 as a development test
# The standalone run_hanoi_experiment() function is a development test runner
# the dissertation's main results come from run_all_experiments.py
if __name__ == "__main__":
    n = 5
    print(f"Running Hanoi recursive with n={n}...")
    hanoi_recursive(n, "A", "C", "B")
    print("Recursive done.")

    print(f"Running Hanoi iterative with n={n}...")
    hanoi_iterative(n, "A", "C", "B")
    print("Iterative done.")
    print()


    run_hanoi_experiment()