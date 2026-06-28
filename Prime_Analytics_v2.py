# ======================
# IMPORTS
# ======================
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt


# ======================
# SIEVE (OPTIMIZED VERSION)
# ======================
def criba(n):
    es_primo = np.ones(n + 1, dtype=bool)
    es_primo[:2] = False

    for i in range(2, int(np.sqrt(n)) + 1):
        if es_primo[i]:
            es_primo[i*i:n+1:i] = False

    return np.where(es_primo)[0]


# ======================
# PRIME GENERATION
# ======================
n = 20_000_000

start = time.time()
primos = criba(n)
end = time.time()


# ======================
# DATASET
# ======================
df = pd.DataFrame(primos, columns=["prime"])

df["index"] = df.index + 1
df["gap"] = df["prime"].diff()

df["log_n"] = np.log(df["prime"])
df["ratio"] = df["prime"] / df["log_n"]

df["density_real"] = df["index"] / df["prime"]
df["density_teo"] = 1 / df["log_n"]

df["error"] = df["density_real"] - df["density_teo"]

# media móvil
df["gap_ma"] = df["gap"].rolling(window=1000).mean()


# ======================
# LOGARITHM BINS
# ======================
bins = np.logspace(
    np.log10(df["prime"].min()),
    np.log10(df["prime"].max()),
    20
)

df["bin"] = pd.cut(df["prime"], bins=bins)
gap_mean = df.groupby("bin")["gap"].mean()


# ======================
# 🔹 1. DENSITY
# ======================
plt.figure(figsize=(10, 6))

# Empirical density (points)
plt.scatter(df["prime"], df["density_real"], s=3, alpha=0.6, label="Empirical")

# Theoretical density (line)
plt.plot(df["prime"], df["density_teo"], color="red", label="Theoretical (1/log n)")

plt.xscale("log")

plt.xlabel("n")
plt.ylabel("Density")
plt.title(f"Prime Density vs Theoretical Model (n = {n:,})")

plt.legend()
plt.tight_layout()

plt.savefig("densidad_primos.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# 🔹 2. ERROR
# ======================
plt.figure(figsize=(10, 6))

# Error line
plt.plot(df["prime"], df["error"], alpha=0.6, label="Error")

# Scatter points
plt.scatter(df["prime"], df["error"], s=3)

# Reference line
plt.axhline(0, color="red", linestyle="--", label="Zero Line")

plt.xscale("log")

plt.xlabel("n")
plt.ylabel("Error")
plt.title("Error: Empirical vs Theoretical Density")

plt.legend()
plt.tight_layout()

plt.savefig("error_densidad.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# 🔹 3. GAP DISTRIBUTION
# ======================
plt.figure(figsize=(10, 6))

plt.hist(df["gap"].dropna(), bins=50, density=True)

plt.xlabel("Gap")
plt.ylabel("Frequency")
plt.title(f"Gap Distribution (n = {n:,})")

plt.tight_layout()

plt.savefig("hist_gaps.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# 🔹 4. PRIME GAPS (SCATTER)
# ======================
plt.figure(figsize=(10, 6))

plt.scatter(df["index"], df["gap"], s=2, alpha=0.4)

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Prime Index")
plt.ylabel("Gap")
plt.title("Prime Gaps vs Prime Index (Log-Log Scale)")

plt.tight_layout()

plt.savefig("gap_scatter.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# 🔹 5. GAPS BY BINS
# ======================
plt.figure(figsize=(10, 6))

gap_mean.plot(label="Average Gap")

plt.xticks(rotation=45)

plt.xlabel("n (log scale bins)")
plt.ylabel("Average Gap")
plt.title("Average Prime Gap by Logarithmic Bins")

plt.legend()
plt.tight_layout()

plt.savefig("gap_bins.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# 🔹 6. GAP VS LOG (MA)
# ======================
plt.figure(figsize=(10, 6))

df_plot = df[df["prime"] >= 10000]

plt.plot(df_plot["prime"], df_plot["gap_ma"], label="Average Gap (MA)")
plt.plot(df_plot["prime"], np.log(df_plot["prime"]), label="log(n)", linestyle="--")

plt.xscale("log")

plt.xlabel("n")
plt.ylabel("Value")
plt.title("Average Gap vs log(n) (n ≥ 10,000)")

plt.legend()
plt.tight_layout()

plt.savefig("gap_vs_log.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# 🔹 7. BINS VS LOG (LOG-LOG)
# ======================

# ======================
# 🔹 7. BINS VS LOG (LOG-LOG)
# ======================

bin_centers = [interval.mid for interval in gap_mean.index]

plt.figure(figsize=(10, 6))

plt.plot(bin_centers, gap_mean, label="Average Gap")
plt.plot(bin_centers, np.log(bin_centers), label="log(n)", linestyle="--")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("n (log scale)")
plt.ylabel("Value")
plt.title("Average Gap vs log(n) (Log-Log Scale)")

plt.legend()
plt.tight_layout()

plt.savefig("gap_bins_vs_log.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# 🔹 8. GAP VS LOG (DISCRETE)
# ======================
n_values = [10_000, 50_000, 100_000, 500_000, 1_000_000]

gap_promedios = []

for val in n_values:
    primos_n = primos[primos <= val]
    gaps = np.diff(primos_n)
    gap_promedios.append(gaps.mean())

plt.figure(figsize=(10, 6))

plt.plot(n_values, gap_promedios, marker='o', label='Average Gap')
plt.plot(n_values, np.log(n_values), marker='s', label='log(n)')

plt.xscale('log')

plt.xlabel('n')
plt.ylabel('Value')
plt.title('Average Gap vs log(n) (Discrete Sample Points)')

plt.legend()
plt.tight_layout()

plt.savefig('gap_promedio_vs_log.png', dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# 🔹 9. GAP DISTRIBUTION (SCALES)
# ======================
n_values = [10_000, 100_000, 1_000_000]

plt.figure(figsize=(10, 6))

for val in n_values:
    primos_n = primos[primos <= val]
    gaps = np.diff(primos_n)

    plt.hist(gaps, bins=50, density=True, alpha=0.5, label=f'n = {val:,}')

plt.xlabel('Gap')
plt.ylabel('Density')
plt.title('Gap Distribution Across Different Scales')

plt.legend()
plt.tight_layout()

plt.savefig('distribucion_gaps_comparada.png', dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# 🔹 10. GAP DISTRIBUTION (LINES)
# ======================
plt.figure(figsize=(10, 6))

for val in n_values:
    primos_n = primos[primos <= val]
    gaps = np.diff(primos_n)

    unique_gaps, counts = np.unique(gaps, return_counts=True)
    density = counts / counts.sum()

    plt.plot(unique_gaps, density, label=f'n = {val:,}')

plt.xlabel('Gap')
plt.ylabel('Relative Frequency')
plt.title('Gap Distribution (Line Representation)')

plt.legend()
plt.tight_layout()

plt.savefig('distribucion_gaps_lineas.png', dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# 🔹 11. NORMALIZED GAPS
# ======================
plt.figure(figsize=(10, 6))

for val in n_values:
    primos_n = primos[primos <= val]
    gaps = np.diff(primos_n)

    gaps_norm = gaps / np.log(val)

    unique_gaps, counts = np.unique(gaps_norm.round(2), return_counts=True)
    density = counts / counts.sum()

    plt.plot(unique_gaps, density, label=f'n = {val:,}')

plt.xlabel('Gap / log(n)')
plt.ylabel('Relative Frequency')
plt.title('Normalized Gap Distribution')

plt.legend()
plt.tight_layout()

plt.savefig('distribucion_gaps_normalizados.png', dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("\n" * 3)

# ======================
# BENCHMARK
# ======================
print(f"Tiempo total: {end - start:.2f} segundos")
