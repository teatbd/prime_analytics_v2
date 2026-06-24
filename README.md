# 📊 Prime Analytics v2 — Empirical Analysis of Prime Numbers

---

# 🚀 Overview

This project explores the behavior of prime numbers from a data-driven perspective.

It started with a simple question:

> Do prime numbers follow any pattern?

By generating primes at scale and analyzing their properties, this project reveals that although primes appear irregular locally, they follow clear statistical laws globally.

---

# 🎯 Objective

The analysis focuses on:

- Prime density  
- Error vs theoretical approximation  
- Distribution of gaps between primes  
- Relationship between primes and logarithmic growth  

---

# ⚙️ Data Generation

Prime numbers are generated using an optimized version of the **Sieve of Eratosthenes**, implemented with NumPy:

```python
def criba(n):
    es_primo = np.ones(n + 1, dtype=bool)
    es_primo[:2] = False

    for i in range(2, int(np.sqrt(n)) + 1):
        if es_primo[i]:
            es_primo[i*i:n+1:i] = False

    return np.where(es_primo)[0]

✅ Key improvement
This version uses vectorized slicing with NumPy, eliminating multiples in bulk rather than iterating element by element.
This significantly improves performance for large values of n.

📌 Dataset size

n = 20,000,000

📊 Example Visualization
plots/gap_vs_log.png

📊 Dataset Structure

| Column  | Description                           |
| ------- | ------------------------------------- |
| `prime` | Prime number                          |
| `index` | Position of the prime (π(n))          |
| `gap`   | Difference between consecutive primes |


🧩 Feature Engineering
📈 Theoretical relationships

log_n = log(n)
density_real = index / prime
density_teo = 1 / log(n)
error = density_real - density_teo

This connects directly with the Prime Number Theorem:
\[
\pi(n) \sim \frac{n}{\log(n)}
\]
``

📐 Gap analysis

gap = difference between primes
gap_ma = rolling mean

This allows analyzing the local structure of primes.

📊 Analysis & Results
🔹 1. Density (Real vs Theoretical)
densidad_primos.png

Real: π(n) / n
Theoretical: 1 / log(n)

✅ Conclusion:
Both curves converge as n increases.

🔹 2. Error Analysis
error_densidad.png
✅ Conclusion:

Error decreases with n
Oscillations become smaller
The model improves at scale


🔹 3. Gap Distribution
hist_gaps.png
✅ Insight:

Many small gaps
Few large gaps
Right-skewed distribution with long tail


🔹 4. Gap Evolution vs log(n)
gap_vs_log.png
✅ Key result:
Average gap∼log⁡(n)\text{Average gap} \sim \log(n)Average gap∼log(n)

🔥 Key Insights
✅ Density
Prime numbers become less frequent as:
density∼1log⁡(n)\text{density} \sim \frac{1}{\log(n)}density∼log(n)1​

✅ Gap behavior

Gaps increase on average
Small gaps persist at all scales
Large gaps become less frequent


✅ Distribution

Right-skewed
Long tail
Stable shape across scales


✅ Important clarification
✔️ Correct:

Frequency of large gaps decreases

❌ Incorrect:

Probability decreases


💥 Final Interpretation
Prime numbers exhibit:

❌ Local irregularity
✅ Global structure

"Primes appear chaotic individually, but follow clear statistical laws at scale."

📁 Project Structure
prime-analytics-v2/
│
├── prime_analytics_v2.py
├── plots/
│   ├── densidad_primos.png
│   ├── error_densidad.png
│   ├── hist_gaps.png
│   ├── gap_vs_log.png
│   └── ...
└── README.md

⏱️ Performance
n = 20,000,000
Execution time: (varies by machine)

🚀 Key Takeaways

Generated primes up to 20M ✅
Validated density ~ 1/log(n) ✅
Observed decreasing error ✅
Analyzed gap distribution ✅
Confirmed gap growth ~ log(n) ✅


🧠 Final Thought
This project evolved from a simple question:

What are prime numbers?

Into an empirical exploration showing that:

even seemingly random systems can reveal deep and consistent patterns.
​
