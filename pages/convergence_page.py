import pandas as pd
import streamlit as st

from components.greek_helpers import inject_custom_css
from components.sidebar import render_sidebar
from models import binomial as binom
from models import black_scholes as bs
from visualizations import convergence

inject_custom_css()

params = render_sidebar(show_steps=True)
S, K, T, r, sigma = params["S"], params["K"], params["T"], params["r"], params["sigma"]
opt = params["option_type"]
N = params["N"]

st.title("Convergence: Binomial to Black-Scholes")
st.caption(
    "Both models price European options. As the number of binomial steps increases, "
    "the discrete binomial price converges to the continuous Black-Scholes price."
)

bs_price = bs.price(S, K, T, r, sigma, opt)
bin_price = binom.price(S, K, T, r, sigma, N, opt)

col1, col2, col3 = st.columns(3)
col1.metric("Black-Scholes Price", f"{bs_price:.4f}")
col2.metric(f"Binomial Price (N={N})", f"{bin_price:.4f}")
col3.metric("Difference", f"{abs(bs_price - bin_price):.6f}")

max_steps = st.slider("Max steps to plot", 10, 500, 200, step=10)
with st.spinner("Computing convergence..."):
    fig = convergence.convergence_chart(S, K, T, r, sigma, opt, max_steps)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Greeks Comparison")
bs_greeks = bs.all_greeks(S, K, T, r, sigma, opt)
bin_greeks = binom.greeks_finite_difference(S, K, T, r, sigma, N, opt)

greek_names = ["delta", "gamma", "theta", "vega", "rho"]
bin_col = f"Binomial (N={N})"
comparison = pd.DataFrame(
    {
        "Greek": [g.title() for g in greek_names],
        "Black-Scholes": [bs_greeks[g] for g in greek_names],
        bin_col: [bin_greeks[g] for g in greek_names],
    }
)
comparison["Difference"] = abs(comparison["Black-Scholes"] - comparison[bin_col])
st.dataframe(
    comparison.style.format(
        {"Black-Scholes": "{:.6f}", bin_col: "{:.6f}", "Difference": "{:.6f}"}
    ),
    use_container_width=True,
)
