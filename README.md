# Options Pricing Explorer

An interactive Streamlit application for exploring options pricing models, visualizing Greeks, and comparing analytical and numerical methods side by side.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at [http://localhost:8501](http://localhost:8501).

## Requirements

- Python 3.10+
- streamlit >= 1.39.0
- numpy >= 1.26.0
- scipy >= 1.12.0
- plotly >= 5.18.0

---

## Application Pages

### 1. Home

Landing page with an overview of each pricing model and a reference table of the Greeks.

---

### 2. Black-Scholes Model

Analytical closed-form pricing for European vanilla options using the Black-Scholes-Merton framework.

#### Assumptions

- The underlying asset follows geometric Brownian motion with constant volatility σ and drift r.
- Continuous trading, no transaction costs, no dividends.
- Log-returns are normally distributed: ln(S_T / S_0) ~ N((r - σ²/2)T, σ²T).

#### Core Formulas

**Auxiliary terms:**

$$
d_1 = \frac{\ln(S/K) + (r + \tfrac{1}{2}\sigma^2)\,T}{\sigma\sqrt{T}}
$$

$$
d_2 = d_1 - \sigma\sqrt{T} = \frac{\ln(S/K) + (r - \tfrac{1}{2}\sigma^2)\,T}{\sigma\sqrt{T}}
$$

where:
| Symbol | Description |
|--------|-------------|
| S | Current underlying asset price |
| K | Strike price |
| T | Time to expiration (years) |
| r | Risk-free interest rate (annualized) |
| σ | Volatility (annualized standard deviation of log-returns) |
| N(·) | Standard normal cumulative distribution function |
| n(·) | Standard normal probability density function |

**Option price:**

$$
C = S\,N(d_1) - K\,e^{-rT}\,N(d_2)
$$

$$
P = K\,e^{-rT}\,N(-d_2) - S\,N(-d_1)
$$

#### Greeks (Closed-Form)

| Greek | Call | Put |
|-------|------|-----|
| **Delta** (∂V/∂S) | N(d₁) | N(d₁) − 1 |
| **Gamma** (∂²V/∂S²) | n(d₁) / (Sσ√T) | same as call |
| **Theta** (∂V/∂t) | −Sn(d₁)σ / (2√T) − rKe^(−rT)N(d₂) | −Sn(d₁)σ / (2√T) + rKe^(−rT)N(−d₂) |
| **Vega** (∂V/∂σ) | Sn(d₁)√T × 0.01 | same as call |
| **Rho** (∂V/∂r) | KTe^(−rT)N(d₂) × 0.01 | −KTe^(−rT)N(−d₂) × 0.01 |

> **Note:** Vega and Rho are scaled per 1% move (multiplied by 0.01) so that displayed values represent the price change for a 1 percentage-point shift in volatility or rate.

#### Visualizations

- **Payoff Diagram** — Intrinsic value at expiry (hockey-stick) overlaid with current Black-Scholes value curve.
- **Greeks vs Underlying** — 3×2 subplot grid showing each Greek as a function of the underlying asset price.
- **Price Sensitivity Heatmap** — Option price across a grid of underlying prices and volatilities.

#### Exercise Style Note

The Black-Scholes model only prices European options. If American exercise is selected on this page, a warning is displayed directing the user to the Binomial model.

---

### 3. Binomial Model (Cox-Ross-Rubinstein)

A discrete-time lattice model that builds a recombining binomial tree of possible asset prices. Supports both **European** and **American** exercise styles.

#### CRR Tree Construction

Given N time steps, the tree parameters are:

$$
\Delta t = \frac{T}{N}
$$

$$
u = e^{\sigma\sqrt{\Delta t}}, \quad d = \frac{1}{u} = e^{-\sigma\sqrt{\Delta t}}
$$

$$
p = \frac{e^{r\,\Delta t} - d}{u - d}
$$

where:
| Symbol | Description |
|--------|-------------|
| Δt | Length of each time step |
| u | Up-move factor |
| d | Down-move factor (d = 1/u ensures the tree recombines) |
| p | Risk-neutral probability of an up-move |

**Asset price at node (i, j):**

$$
S_{i,j} = S_0 \cdot u^{j-i} \cdot d^{i}
$$

where j is the time step (0 to N) and i is the number of down-moves (0 to j).

#### Backward Induction

**At expiry (j = N):**

$$
V_{i,N} = \max(S_{i,N} - K,\; 0) \quad \text{(call)}, \qquad V_{i,N} = \max(K - S_{i,N},\; 0) \quad \text{(put)}
$$

**Working backward (j = N−1 down to 0):**

$$
V_{i,j}^{\text{cont}} = e^{-r\,\Delta t}\left[p\,V_{i,j+1} + (1-p)\,V_{i+1,j+1}\right]
$$

For **European** exercise:

$$
V_{i,j} = V_{i,j}^{\text{cont}}
$$

For **American** exercise, the holder can exercise early:

$$
V_{i,j} = \max\!\left(V_{i,j}^{\text{cont}},\;\text{intrinsic}_{i,j}\right)
$$

The option price is V₀,₀.

#### Greeks (Finite Difference)

Since the binomial model has no closed-form Greeks, they are computed numerically via central differences:

$$
\Delta \approx \frac{V(S+h) - V(S-h)}{2h}, \quad h = 0.01 \cdot S
$$

$$
\Gamma \approx \frac{V(S+h) - 2V(S) + V(S-h)}{h^2}
$$

$$
\Theta \approx \frac{V(S,\,T - \tfrac{1}{365}) - V(S,\,T)}{\tfrac{1}{365}}
$$

$$
\mathcal{V} \approx \frac{V(\sigma + 0.001) - V(\sigma - 0.001)}{0.002} \times 0.01
$$

$$
\rho \approx \frac{V(r + 0.0001) - V(r - 0.0001)}{0.0002} \times 0.01
$$

#### Performance

`binomial.price()` is decorated with `@functools.lru_cache(maxsize=2048)` to avoid recomputing identical trees during Greek finite-difference bumps and convergence sweeps.

#### Visualizations

- **Binomial Tree** — Interactive Plotly scatter plot of the asset/option lattice (capped at 15 displayed steps; full tree used for pricing).
- **Greeks vs Underlying** — Same 3×2 grid as Black-Scholes, using finite-difference Greeks.
- **Payoff Diagram** — Intrinsic value overlaid with current binomial value.

---

### 4. Binary / Digital Option

Cash-or-nothing options that pay a fixed amount if in the money at expiration, and nothing otherwise. European exercise only.

#### Payoff at Expiry

Unlike vanilla options with a "hockey-stick" payoff, binary options have a **step-function** payoff:

$$
\text{Payoff}_{\text{call}} = \begin{cases} 1 & \text{if } S_T > K \\ 0 & \text{if } S_T \leq K \end{cases}
$$

$$
\text{Payoff}_{\text{put}} = \begin{cases} 1 & \text{if } S_T < K \\ 0 & \text{if } S_T \geq K \end{cases}
$$

#### Pricing

The price is the discounted risk-neutral probability of finishing in the money:

$$
C_{\text{binary}} = e^{-rT}\,N(d_2)
$$

$$
P_{\text{binary}} = e^{-rT}\,N(-d_2)
$$

where d₂ is the same as in the Black-Scholes formula above.

**Intuition:** N(d₂) is the risk-neutral probability that S_T > K. The factor e^(−rT) discounts this expected payoff back to today.

#### Greeks

| Greek | Call | Put |
|-------|------|-----|
| **Delta** | e^(−rT) · n(d₂) / (Sσ√T) | −e^(−rT) · n(−d₂) / (Sσ√T) |
| **Gamma** | −e^(−rT) · n(d₂) · d₁ / (S²σ²T) | e^(−rT) · n(−d₂) · d₁ / (S²σ²T) |
| **Theta** | Finite difference: [V(T − 1/365) − V(T)] / (1/365) |
| **Vega** | Finite difference (per 1% vol move) |
| **Rho** | Finite difference (per 1% rate move) |

> Delta and Gamma have analytical forms. Theta, Vega, and Rho use central finite differences because their analytical expressions for binary options are complex and error-prone.

#### Visualizations

- **Payoff Diagram** — Step-function payoff at expiry overlaid with the smooth current-value curve (sigmoid shape).
- **Greeks vs Underlying** — 3×2 grid. Note that binary Delta peaks sharply near the strike and binary Gamma changes sign at the strike.
- **Price Sensitivity Heatmap** — Binary option price across underlying prices and volatilities.

---

### 5. Binary Spread

A combination strategy that pairs a **binary call** at an upper strike with a **binary put** at a lower strike. The position profits when the underlying asset moves significantly in either direction away from the range defined by the two strikes.

#### Structure

| Leg | Type | Strike | Pays 1 if... |
|-----|------|--------|--------------|
| Leg 1 | Binary Call | K_call (upper) | S_T > K_call |
| Leg 2 | Binary Put | K_put (lower) | S_T < K_put |

Default parameters: S = 75, K_call = 80, K_put = 70.

#### Combined Payoff at Expiry

$$
\text{Payoff}_{\text{spread}} = \mathbb{1}_{S_T > K_{\text{call}}} + \mathbb{1}_{S_T < K_{\text{put}}}
$$

This produces three regions:

| Region | Condition | Payoff |
|--------|-----------|--------|
| Below lower strike | S_T < K_put | 1 (put leg pays) |
| Between strikes | K_put ≤ S_T ≤ K_call | 0 (neither leg pays) |
| Above upper strike | S_T > K_call | 1 (call leg pays) |

#### Pricing

Each leg is priced independently using the binary option formula:

$$
V_{\text{call leg}} = e^{-rT}\,N(d_2^{\text{call}})
$$

$$
V_{\text{put leg}} = e^{-rT}\,N(-d_2^{\text{put}})
$$

where:

$$
d_2^{\text{call}} = \frac{\ln(S/K_{\text{call}}) + (r - \tfrac{1}{2}\sigma^2)\,T}{\sigma\sqrt{T}}
$$

$$
d_2^{\text{put}} = \frac{\ln(S/K_{\text{put}}) + (r - \tfrac{1}{2}\sigma^2)\,T}{\sigma\sqrt{T}}
$$

**Combined spread price:**

$$
V_{\text{spread}} = V_{\text{call leg}} + V_{\text{put leg}} = e^{-rT}\left[N(d_2^{\text{call}}) + N(-d_2^{\text{put}})\right]
$$

#### P&L at Expiry

$$
\text{Net P\&L} = \text{Payoff}_{\text{spread}} - V_{\text{spread}}
$$

| Scenario | Payout | Cost | Net P&L |
|----------|--------|------|---------|
| S_T < K_put | 1.00 | V_spread | 1 − V_spread |
| K_put ≤ S_T ≤ K_call | 0.00 | V_spread | −V_spread |
| S_T > K_call | 1.00 | V_spread | 1 − V_spread |

Maximum loss is the cost of the spread (when the asset stays between the strikes). Maximum gain is 1 minus the cost.

#### Combined Greeks

The Greeks of the spread are the sum of the individual leg Greeks:

$$
\Delta_{\text{spread}} = \Delta_{\text{call leg}} + \Delta_{\text{put leg}}
$$

$$
\Gamma_{\text{spread}} = \Gamma_{\text{call leg}} + \Gamma_{\text{put leg}}
$$

and likewise for Theta, Vega, and Rho.

At the midpoint between strikes with symmetric parameters, Delta should be near zero (the position is approximately delta-neutral), though the log-normal pricing model introduces a slight asymmetry (see note below).

#### Why the Combined Value Curve Is Not Perfectly Symmetric

Even when the two strikes are equidistant from the spot price (e.g., K_put = 70, S = 75, K_call = 80), the combined value curve is not perfectly symmetric. This is **not a bug** — it arises from two properties of the Black-Scholes framework:

1. **Log-normal distribution:** The model prices options in log-space, where the midpoint between K_put and K_call is the *geometric mean* √(K_put · K_call), not the arithmetic mean (K_put + K_call)/2. For strikes 70 and 80: √(70 × 80) ≈ 74.83, which is left of 75.

2. **Variance correction (−σ²/2 drift):** Even with r = 0, the d₂ formula contains a −σ²/2 term. This is the Itô correction that ensures e^(σW − σ²t/2) is a martingale. It shifts probability mass slightly downward in log-space, making the put leg marginally more valuable than the call leg at the arithmetic midpoint.

To observe near-perfect symmetry, set the spot to the geometric mean of the two strikes.

#### Visualizations

- **Payoff Diagram** — Four traces: combined payoff at expiry (dashed), individual call and put leg values (dotted), and combined current value (solid).
- **P&L at Expiry Table** — Tabulated scenarios with payout, cost, and net P&L for each region.

---

### 6. Convergence: Binomial → Black-Scholes

Demonstrates that as the number of binomial steps N → ∞, the discrete binomial price converges to the continuous Black-Scholes price. Both models price European options.

#### Convergence Property

$$
\lim_{N \to \infty} V_{\text{binomial}}(N) = V_{\text{BS}}
$$

The convergence is O(1/N) and oscillates around the true value (odd and even N approach from opposite sides).

#### Visualizations

- **Price Comparison Metrics** — Side-by-side display of BS price, Binomial price at current N, and their absolute difference.
- **Convergence Chart** — Binomial price plotted against step count (up to a configurable maximum), with a horizontal line at the BS price.
- **Greeks Comparison Table** — DataFrame comparing all five Greeks from both models, with absolute differences.

---

## Project Structure

```
options-models/
├── app.py                          # Entry point — page routing
├── requirements.txt
├── .streamlit/
│   └── config.toml                 # toolbarMode = "viewer"
├── components/
│   ├── sidebar.py                  # Shared sidebar inputs
│   └── greek_helpers.py            # Shared Greek definitions, metrics display, CSS
├── models/
│   ├── black_scholes.py            # Analytical BS pricing + closed-form Greeks
│   ├── binomial.py                 # CRR tree + finite-difference Greeks
│   └── binary.py                   # Binary option pricing + Greeks
├── pages/
│   ├── home_page.py                # Landing page
│   ├── black_scholes_page.py       # BS model page
│   ├── binomial_page.py            # Binomial model page
│   ├── binary_page.py              # Binary/digital option page
│   ├── binary_spread_page.py       # Binary spread strategy page
│   └── convergence_page.py         # Binomial-to-BS convergence
└── visualizations/
    ├── greeks_charts.py            # 3×2 Greeks subplot grid
    ├── payoff_diagrams.py          # Vanilla, binary, and spread payoff charts
    ├── sensitivity.py              # Price sensitivity heatmap
    ├── convergence.py              # Convergence line chart
    └── tree_plot.py                # Binomial lattice visualization
```

## Shared Parameters

All pages (except Binary Spread, which has its own sidebar) share a common sidebar with these inputs:

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| Option Type | Call | Call / Put | Radio toggle |
| Exercise Style | American | American / European | Shown on BS and Binomial pages |
| Underlying Asset Price (S) | 75.0 | ≥ 1.0 | |
| Strike (K) | 75.0 | ≥ 1.0 | |
| Time to Expiry | 52 weeks | 1–156 weeks | Converted to years internally (T = weeks/52) |
| Volatility (σ) | 0.20 | 0.01–1.50 | |
| Risk-Free Rate (r) | 0.05 | 0.00–0.20 | |
| Binomial Steps (N) | 50 | 1–200 | Binomial and Convergence pages only |

A **Reset to Defaults** button clears all session state and reruns the app.

## Notation Reference

| Symbol | Meaning |
|--------|---------|
| S, S₀ | Current underlying asset price |
| S_T | Underlying asset price at expiration |
| K | Strike price |
| T | Time to expiration (years) |
| r | Annualized risk-free interest rate |
| σ | Annualized volatility |
| N(x) | CDF of the standard normal distribution |
| n(x) | PDF of the standard normal distribution |
| C, P | Call price, Put price |
| V | Option value (generic) |
| 𝟙 | Indicator function (1 if condition true, 0 otherwise) |
| Δt | Binomial time step = T/N |
| u, d | Binomial up/down factors |
| p | Risk-neutral up-move probability |
