import numpy as np
import streamlit as st

from components.greek_helpers import BINARY_GREEK_HELP, inject_custom_css
from models import binary
from visualizations import payoff_diagrams

inject_custom_css()

st.title("Binary Spread")
st.caption(
    "Combines a binary call at one strike with a binary put at a lower strike. "
    "Profits when the underlying moves significantly in either direction."
)

st.sidebar.header("Spread Parameters")

if st.sidebar.button("Reset to Defaults"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

S = st.sidebar.number_input(
    "Underlying Asset Price (S)", min_value=1.0, value=75.0, step=1.0
)
K_call = st.sidebar.number_input(
    "Call Strike (upper)", min_value=1.0, value=80.0, step=1.0
)
K_put = st.sidebar.number_input(
    "Put Strike (lower)", min_value=1.0, value=70.0, step=1.0
)
T_weeks = st.sidebar.slider(
    "Time to Expiry (weeks)", min_value=1, max_value=156, value=52, step=1
)
T = T_weeks / 52.0
sigma = st.sidebar.slider(
    "Volatility (σ)", min_value=0.01, max_value=1.50, value=0.20, step=0.01
)
r = st.sidebar.slider(
    "Risk-Free Rate (r)", min_value=0.0, max_value=0.20, value=0.05, step=0.005
)

with st.expander("Model Equations"):
    st.markdown("**Structure:** Binary Call at $K_{\\text{call}}$ + Binary Put at $K_{\\text{put}}$")
    st.markdown("**Individual Leg Pricing**")
    st.latex(r"d_2^{\text{call}} = \frac{\ln(S/K_{\text{call}}) + (r - \tfrac{1}{2}\sigma^2)\,T}{\sigma\sqrt{T}}")
    st.latex(r"d_2^{\text{put}} = \frac{\ln(S/K_{\text{put}}) + (r - \tfrac{1}{2}\sigma^2)\,T}{\sigma\sqrt{T}}")
    st.latex(r"V_{\text{call}} = e^{-rT}\,N(d_2^{\text{call}}), \quad V_{\text{put}} = e^{-rT}\,N(-d_2^{\text{put}})")
    st.markdown("**Combined Spread Price**")
    st.latex(r"V_{\text{spread}} = e^{-rT}\left[N(d_2^{\text{call}}) + N(-d_2^{\text{put}})\right]")
    st.markdown("**Payoff at Expiry**")
    st.latex(r"\text{Payoff} = \mathbb{1}_{S_T > K_{\text{call}}} + \mathbb{1}_{S_T < K_{\text{put}}}")
    st.markdown("**P&L**")
    st.latex(r"\text{Net P\&L} = \text{Payoff} - V_{\text{spread}}")

# Price each leg
call_price = binary.price(S, K_call, T, r, sigma, "call")
put_price = binary.price(S, K_put, T, r, sigma, "put")
combined_price = call_price + put_price

col1, col2, col3 = st.columns(3)
col1.metric(
    f"Binary Call (K={K_call:.0f})",
    f"{call_price:.4f}",
    help="Price of the binary call leg.",
)
col2.metric(
    f"Binary Put (K={K_put:.0f})",
    f"{put_price:.4f}",
    help="Price of the binary put leg.",
)
col3.metric(
    "Combined Spread Price",
    f"{combined_price:.4f}",
    help="Total cost of the spread (sum of both legs).",
)

# Greeks for each leg and combined
call_greeks = binary.all_greeks(S, K_call, T, r, sigma, "call")
put_greeks = binary.all_greeks(S, K_put, T, r, sigma, "put")

show_greeks = st.toggle("Show Greeks", value=True)

if show_greeks:
    st.subheader("Combined Greeks")
    greek_names = ["delta", "gamma", "theta", "vega", "rho"]
    cols = st.columns(5)
    for col, g in zip(cols, greek_names):
        combined_val = call_greeks[g] + put_greeks[g]
        col.metric(
            g.title(),
            f"{combined_val:.4f}",
            help=BINARY_GREEK_HELP.get(g.title(), ""),
        )

# Payoff diagram
st.subheader("Payoff Diagram")
fig = payoff_diagrams.spread_payoff_diagram(S, K_call, K_put, T, r, sigma, binary.price)
st.plotly_chart(fig, use_container_width=True)

# P&L at expiry
st.subheader("P&L at Expiry")
st.markdown(f"""
| Scenario | Payout | Cost | Net P&L |
|----------|--------|------|---------|
| Asset < {K_put:.0f} (put pays) | 1.00 | {combined_price:.4f} | {1.0 - combined_price:+.4f} |
| {K_put:.0f} ≤ Asset ≤ {K_call:.0f} (neither pays) | 0.00 | {combined_price:.4f} | {0.0 - combined_price:+.4f} |
| Asset > {K_call:.0f} (call pays) | 1.00 | {combined_price:.4f} | {1.0 - combined_price:+.4f} |
""")
