import streamlit as st
from components.greek_helpers import inject_custom_css

inject_custom_css()

st.title("Options Pricing Explorer")

st.markdown("""
This app lets you interactively explore options pricing models
and compare their behavior across different market conditions.

---

### Models

**Black-Scholes** — The classic analytical model for pricing European options.
Assumes constant volatility, log-normal underlying asset prices, and continuous trading.
Provides closed-form solutions for price and all Greeks.

**Binomial (CRR)** — A discrete-time lattice model that builds a tree of possible
underlying asset prices. Supports both European and American exercise styles. As the number
of steps increases, it converges to the Black-Scholes price.

**Binary / Digital** — Options that pay a fixed amount if they expire
in the money, and nothing otherwise. Also called "cash-or-nothing" options.
Priced analytically using the Black-Scholes framework.

**Binary Spread** — A combination strategy pairing a binary call at one strike
with a binary put at a lower strike. Profits when the underlying moves significantly
in either direction.

---

### Greeks

| Greek | What it measures |
|-------|-----------------|
| **Delta** | Price sensitivity to a $1 move in the underlying asset |
| **Gamma** | Rate of change of Delta (curvature of the price curve) |
| **Theta** | Time decay — value lost per day as expiration approaches |
| **Vega** | Sensitivity to a 1% change in implied volatility |
| **Rho** | Sensitivity to a 1% change in the risk-free interest rate |

---

Use the sidebar to navigate between models and adjust parameters.
""")
