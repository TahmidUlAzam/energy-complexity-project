# green_algorithms_validation.py - cross-validation script for this dissertation.
# This script applies the Green Algorithms formula proposed by Lannelongue et al.
# to all 52 configurations in summary_statistics.csv and compares the estimates
# against the CodeCarbon measurements reported in Chapter 5.

import pandas as pd

# Green Algorithms formula (Lannelongue et al., 2021):
# E = t * (n_c * P_c * u_c + n_m * P_m) * PUE * 0.001
# E   = energy consumption in kWh
# t   = running time in hours
# n_c = number of cores in use
# P_c = power draw per core in Watts
# u_c = core usage factor between 0 and 1
# n_m = memory available in GB
# P_m = power draw per GB of memory in Watts per GB
# PUE = power usage effectiveness

# Hardware parameters for the MacBook Pro used in this dissertation.
# The Intel Core i7-9750H has a TDP of 45W across 6 cores which gives
# 7.5W per core. The Python code is single-threaded so only one core
# is in use at a time. The memory power draw of 0.3725 W per GB is
# from the Green Algorithms paper. PUE is 1.0 as the experiments were
# carried out on a personal laptop.
N_CORES = 1
P_CORE = 7.5
U_CORE = 1.0
N_MEMORY_GB = 16
P_MEMORY = 0.3725
PUE = 1.0


# Applies the Green Algorithms formula to convert a runtime
# in seconds into an energy estimate in kWh.
def green_algorithms_energy(duration_seconds):
    t_hours = duration_seconds / 3600
    energy_kwh = t_hours * (N_CORES * P_CORE * U_CORE + N_MEMORY_GB * P_MEMORY) * PUE * 0.001
    return energy_kwh


# Step 1: Load the summary statistics file produced by analyze.py.
df = pd.read_csv("summary_statistics.csv")
print(f"Loaded {len(df)} configurations from summary_statistics.csv")


# Step 2: Apply the Green Algorithms formula to every configuration
# and compute the ratio of the two estimates.
df["ga_energy"] = df["mean_duration"].apply(green_algorithms_energy)
df["ratio"] = df["ga_energy"] / df["mean_energy"]


# Step 3: Print the comparison table for every configuration.
print()
print("=" * 100)
print("COMPARISON: CodeCarbon vs Green Algorithms")
print("=" * 100)
print(f"{'Algorithm':<10} {'Variant':<22} {'n':<6} {'Duration(s)':<13} "
      f"{'CodeCarbon(kWh)':<20} {'GreenAlg(kWh)':<18} {'Ratio':<8}")
print("-" * 100)

for _, row in df.iterrows():
    print(f"{row['algorithm']:<10} {row['variant']:<22} {row['n']:<6} "
          f"{row['mean_duration']:<13.4f} {row['mean_energy']:<20.6e} "
          f"{row['ga_energy']:<18.6e} {row['ratio']:<8.3f}")


# Step 4: Print the summary statistics for the ratios.
print()
print("=" * 100)
print("SUMMARY STATISTICS")
print("=" * 100)
print(f"Mean ratio (Green Algorithms / CodeCarbon):   {df['ratio'].mean():.3f}")
print(f"Median ratio (Green Algorithms / CodeCarbon): {df['ratio'].median():.3f}")
print(f"Minimum ratio:                                {df['ratio'].min():.3f}")
print(f"Maximum ratio:                                {df['ratio'].max():.3f}")
print(f"Standard deviation:                           {df['ratio'].std():.3f}")

print()
print("Per-algorithm summary:")
for alg in df["algorithm"].unique():
    sub = df[df["algorithm"] == alg]
    print(f"  {alg:<12} mean ratio: {sub['ratio'].mean():.3f}   "
          f"median: {sub['ratio'].median():.3f}   (n={len(sub)} configurations)")


# Step 5: Save the full comparison to a CSV file for use in Chapter 5.
df.to_csv("green_algorithms_comparison.csv", index=False)
print()
print("Full comparison saved to green_algorithms_comparison.csv")