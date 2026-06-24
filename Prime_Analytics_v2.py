# ======================
# IMPORTS
# ======================
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt


# ======================
# CRIBA (VERSIÓN OPTIMIZADA)
# ======================
def criba(n):
    es_primo = np.ones(n + 1, dtype=bool)
    es_primo[:2] = False

    for i in range(2, int(np.sqrt(n)) + 1):
        if es_primo[i]:
            es_primo[i*i:n+1:i] = False

    return np.where(es_primo)[0]


# ======================
# GENERACIÓN DE PRIMOS
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
# BINS LOGARÍTMICOS
# ======================
bins = np.logspace(
    np.log10(df["prime"].min()),
    np.log10(df["prime"].max()),
    20
)

df["bin"] = pd.cut(df["prime"], bins=bins)
gap_mean = df.groupby("bin")["gap"].mean()


# ======================
# 🔹 1. DENSIDAD
# ======================
plt.figure(figsize=(10, 6))

plt.plot(df["prime"], df["density_teo"], color="red", label="Teórica (1/log n)")
plt.scatter(df["prime"], df["density_real"], s=3, alpha=0.6, label="Real")

plt.xscale("log")
plt.xlabel("n")
plt.ylabel("Densidad")
plt.title(f"Densidad de primos (n={n:,})")

plt.legend()
plt.savefig("densidad_primos.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()


# ======================
# 🔹 2. ERROR
# ======================
plt.figure(figsize=(10, 6))

plt.plot(df["prime"], df["error"], alpha=0.5)
plt.scatter(df["prime"], df["error"], s=3)

plt.axhline(0, color="red")
plt.xscale("log")

plt.xlabel("n")
plt.ylabel("Error")
plt.title("Error: densidad real vs teórica")

plt.savefig("error_densidad.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()

# ======================
# 🔹 3. HISTOGRAMA GAPS
# ======================
plt.figure(figsize=(10, 6))

plt.hist(df["gap"].dropna(), bins=50)

plt.xlabel("Gap")
plt.ylabel("Frecuencia")
plt.title(f"Distribución de gaps (n={n:,})")

plt.savefig("hist_gaps.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()

# ======================
# 🔹 4. SCATTER GAPS
# ======================
plt.figure(figsize=(10, 6))

plt.scatter(df["index"], df["gap"], s=3)

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Índice del primo")
plt.ylabel("Gap")
plt.title("Gaps entre primos (log-log)")

plt.savefig("gap_scatter.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()

# ======================
# 🔹 5. GAPS POR BINS
# ======================
plt.figure(figsize=(10, 6))

gap_mean.plot()

plt.xticks(rotation=45)
plt.ylabel("Gap promedio")
plt.title("Gap promedio por bins log")

plt.savefig("gap_bins.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()

# ======================
# 🔹 6. GAP VS LOG (MA)
# ======================
plt.figure()

plt.plot(df["prime"], df["gap_ma"], label="Gap promedio (MA)")
plt.plot(df["prime"], np.log(df["prime"]), label="log(n)", linestyle="--")

plt.xscale("log")
plt.xlabel("n")
plt.ylabel("Valor")

plt.title("Gap promedio vs log(n)")
plt.legend()

plt.savefig("gap_vs_log.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()

# ======================
# 🔹 7. BINS VS LOG (LOG-LOG)
# ======================
bin_centers = [interval.mid for interval in gap_mean.index]

plt.figure(figsize=(10, 6))

plt.plot(bin_centers, gap_mean, label="Gap promedio")
plt.plot(bin_centers, np.log(bin_centers), label="log(n)", linestyle="--")

plt.xscale("log")
plt.yscale("log")

plt.legend()
plt.title("Gap medio vs log(n)")

plt.savefig("gap_bins_vs_log.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()

# ======================
# 🔹 8. GAP PROMEDIO VS N (EFICIENTE)
# ======================
n_values = [10_000, 50_000, 100_000, 500_000, 1_000_000]

gap_promedios = []

for val in n_values:
    primos_n = primos[primos <= val]
    gaps = np.diff(primos_n)
    gap_promedios.append(gaps.mean())

plt.figure()

plt.plot(n_values, gap_promedios, marker='o', label='Gap promedio')
plt.plot(n_values, np.log(n_values), marker='s', label='log(n)')

plt.xscale('log')
plt.xlabel('n')
plt.ylabel('Valor')
plt.title('Gap promedio vs log(n)')
plt.legend()

plt.savefig('gap_promedio_vs_log.png')
plt.show()
plt.close()

# ======================
# 🔹 9. DISTRIBUCIÓN NORMALIZADA
# ======================
n_values = [10_000, 100_000, 1_000_000]

plt.figure()

for val in n_values:
    primos_n = primos[primos <= val]
    gaps = np.diff(primos_n)

    plt.hist(gaps, bins=50, density=True, alpha=0.5, label=f'n={val:,}')

plt.xlabel('Gap')
plt.ylabel('Densidad')
plt.title('Distribución de gaps (normalizada)')
plt.legend()

plt.savefig('distribucion_gaps_comparada.png')
plt.show()
plt.close()

# ======================
# 🔹 10. DISTRIBUCIÓN EN LÍNEAS
# ======================
plt.figure()

for val in n_values:
    primos_n = primos[primos <= val]
    gaps = np.diff(primos_n)

    unique_gaps, counts = np.unique(gaps, return_counts=True)
    density = counts / counts.sum()

    plt.plot(unique_gaps, density, label=f'n={val:,}')

plt.xlabel('Gap')
plt.ylabel('Frecuencia relativa')
plt.title('Distribución de gaps (líneas)')
plt.legend()

plt.savefig('distribucion_gaps_lineas.png')
plt.show()
plt.close()

# ======================
# 🔹 11. GAPS NORMALIZADOS
# ======================
plt.figure()

for val in n_values:
    primos_n = primos[primos <= val]
    gaps = np.diff(primos_n)

    gaps_norm = gaps / np.log(val)

    unique_gaps, counts = np.unique(gaps_norm.round(2), return_counts=True)
    density = counts / counts.sum()

    plt.plot(unique_gaps, density, label=f'n={val:,}')

plt.xlabel('Gap / log(n)')
plt.ylabel('Frecuencia relativa')
plt.title('Distribución de gaps normalizados')
plt.legend()

plt.savefig('distribucion_gaps_normalizados.png')
plt.show()
plt.close()

# ======================
# BENCHMARK
# ======================
print(f"Tiempo total: {end - start:.2f} segundos")
