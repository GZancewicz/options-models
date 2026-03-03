import streamlit as st

from components.greek_helpers import BINARY_GREEK_HELP, inject_custom_css, show_greek_metrics
from components.sidebar import render_sidebar
from models import binary
from visualizations import greeks_charts, payoff_diagrams, sensitivity

inject_custom_css()

params = render_sidebar(show_steps=False, show_exercise_style=False)
S, K, T, r, sigma = params["S"], params["K"], params["T"], params["r"], params["sigma"]
opt = params["option_type"]

st.title("Binary / Digital Option")
st.caption(
    "Cash-or-nothing option — pays a fixed amount if in the money at expiration, "
    "nothing otherwise. European exercise only."
)

with st.expander("Model Equations"):
    st.latex(r"d_2 = \frac{\ln(S/K) + (r - \tfrac{1}{2}\sigma^2)\,T}{\sigma\sqrt{T}}")
    st.markdown("**Payoff at Expiry** (step function)")
    st.latex(r"\text{Call} = \begin{cases} 1 & S_T > K \\ 0 & S_T \leq K \end{cases} \qquad \text{Put} = \begin{cases} 1 & S_T < K \\ 0 & S_T \geq K \end{cases}")
    st.markdown("**Option Price** (discounted risk-neutral probability)")
    st.latex(r"C_{\text{binary}} = e^{-rT}\,N(d_2)")
    st.latex(r"P_{\text{binary}} = e^{-rT}\,N(-d_2)")
    st.markdown("**Greeks**")
    st.latex(r"\Delta_C = \frac{e^{-rT}\,n(d_2)}{S\,\sigma\sqrt{T}}")
    st.latex(r"\Gamma_C = -\frac{e^{-rT}\,n(d_2)\,d_1}{S^2\,\sigma^2\,T}")

results = binary.all_greeks(S, K, T, r, sigma, opt)
show_greeks = st.toggle("Show Greeks", value=True)
show_greek_metrics(results, show_greeks, help_dict=BINARY_GREEK_HELP)

if show_greeks:
    tab_payoff, tab_greeks, tab_sensitivity = st.tabs(
        ["Payoff Diagram", "Greeks vs Underlying", "Price Sensitivity"]
    )
else:
    tab_payoff, tab_sensitivity = st.tabs(["Payoff Diagram", "Price Sensitivity"])

with tab_payoff:
    fig = payoff_diagrams.binary_payoff_diagram(S, K, T, r, sigma, opt, binary.price)
    st.plotly_chart(fig, use_container_width=True)

if show_greeks:
    with tab_greeks:
        greek_funcs = {
            "Price": binary.price,
            "Delta": binary.delta,
            "Gamma": binary.gamma,
            "Theta": binary.theta,
            "Vega": binary.vega,
            "Rho": binary.rho,
        }
        fig = greeks_charts.greeks_vs_spot(greek_funcs, S, K, T, r, sigma, opt)
        st.plotly_chart(fig, use_container_width=True)

with tab_sensitivity:
    fig = sensitivity.price_heatmap(K, T, r, sigma, S, opt, binary.price)
    st.plotly_chart(fig, use_container_width=True)
