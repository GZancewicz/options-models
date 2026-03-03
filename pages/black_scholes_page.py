import streamlit as st

from components.greek_helpers import inject_custom_css, show_greek_metrics
from components.sidebar import render_sidebar
from models import black_scholes as bs
from visualizations import greeks_charts, payoff_diagrams, sensitivity

inject_custom_css()

params = render_sidebar(show_steps=False, show_exercise_style=True)
S, K, T, r, sigma = params["S"], params["K"], params["T"], params["r"], params["sigma"]
opt = params["option_type"]
style = params["exercise_style"]

st.title("Black-Scholes Model")
if style == "american":
    st.warning(
        "The Black-Scholes model only prices European options. "
        "Use the Binomial model for American-style pricing."
    )
else:
    st.caption("European option — exercise permitted only at expiration.")

with st.expander("Model Equations"):
    st.latex(r"d_1 = \frac{\ln(S/K) + (r + \tfrac{1}{2}\sigma^2)\,T}{\sigma\sqrt{T}}")
    st.latex(r"d_2 = d_1 - \sigma\sqrt{T}")
    st.markdown("**Option Price**")
    st.latex(r"C = S\,N(d_1) - K\,e^{-rT}\,N(d_2)")
    st.latex(r"P = K\,e^{-rT}\,N(-d_2) - S\,N(-d_1)")
    st.markdown("**Greeks**")
    st.latex(r"\Delta_C = N(d_1), \quad \Delta_P = N(d_1) - 1")
    st.latex(r"\Gamma = \frac{n(d_1)}{S\,\sigma\sqrt{T}}")
    st.latex(r"\Theta_C = -\frac{S\,n(d_1)\,\sigma}{2\sqrt{T}} - r\,K\,e^{-rT}\,N(d_2)")
    st.latex(r"\mathcal{V} = S\,n(d_1)\sqrt{T}")
    st.latex(r"\rho_C = K\,T\,e^{-rT}\,N(d_2)")

results = bs.all_greeks(S, K, T, r, sigma, opt)
show_greeks = st.toggle("Show Greeks", value=True)
show_greek_metrics(results, show_greeks)

if show_greeks:
    tab_payoff, tab_greeks, tab_sensitivity = st.tabs(
        ["Payoff Diagram", "Greeks vs Underlying", "Price Sensitivity"]
    )
else:
    tab_payoff, tab_sensitivity = st.tabs(["Payoff Diagram", "Price Sensitivity"])

with tab_payoff:
    fig = payoff_diagrams.payoff_diagram(S, K, T, r, sigma, opt, bs.price)
    st.plotly_chart(fig, use_container_width=True)

if show_greeks:
    with tab_greeks:
        greek_funcs = {
            "Price": bs.price,
            "Delta": bs.delta,
            "Gamma": bs.gamma,
            "Theta": bs.theta,
            "Vega": bs.vega,
            "Rho": bs.rho,
        }
        fig = greeks_charts.greeks_vs_spot(greek_funcs, S, K, T, r, sigma, opt)
        st.plotly_chart(fig, use_container_width=True)

with tab_sensitivity:
    fig = sensitivity.price_heatmap(K, T, r, sigma, S, opt, bs.price)
    st.plotly_chart(fig, use_container_width=True)
