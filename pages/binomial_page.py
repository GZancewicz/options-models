import numpy as np
import streamlit as st

from components.greek_helpers import GREEK_LABELS, inject_custom_css, show_greek_metrics
from components.sidebar import render_sidebar
from models import binomial as binom
from visualizations import greeks_charts, payoff_diagrams, tree_plot

inject_custom_css()

params = render_sidebar(show_steps=True, show_exercise_style=True)
S, K, T, r, sigma = params["S"], params["K"], params["T"], params["r"], params["sigma"]
opt = params["option_type"]
N = params["N"]
style = params["exercise_style"]

st.title("Binomial Model (CRR)")
if style == "american":
    st.caption(
        "American option — can be exercised at any time before expiration. "
        "Early exercise is checked at every node in the tree."
    )
else:
    st.caption("European option — exercise permitted only at expiration.")

tree_data = binom.build_tree(S, K, T, r, sigma, N, opt, style)
greeks = binom.greeks_finite_difference(S, K, T, r, sigma, N, opt, style)

show_greeks = st.toggle("Show Greeks", value=True)
show_greek_metrics(greeks, show_greeks)

st.caption(
    f"u = {tree_data['u']:.4f}, d = {tree_data['d']:.4f}, "
    f"p = {tree_data['p']:.4f}, dt = {tree_data['dt']:.4f}"
)

if show_greeks:
    tab_tree, tab_greeks, tab_payoff = st.tabs(
        ["Binomial Tree", "Greeks vs Underlying", "Payoff Diagram"]
    )
else:
    tab_tree, tab_payoff = st.tabs(["Binomial Tree", "Payoff Diagram"])

with tab_tree:
    fig = tree_plot.binomial_tree_figure(
        tree_data["stock_tree"], tree_data["option_tree"], N
    )
    st.plotly_chart(fig, use_container_width=True)
    if N > 15:
        st.info(f"Showing first 15 of {N} steps. Full tree used for pricing.")

if show_greeks:
    with tab_greeks:

        def _make_greek_func(greek_name):
            def func(S_arr, K, T, r, sigma, option_type):
                return np.array(
                    [
                        binom.greeks_finite_difference(
                            s, K, T, r, sigma, N, option_type, style
                        )[greek_name]
                        for s in S_arr
                    ]
                )

            return func

        with st.spinner("Computing Greeks..."):
            greek_funcs = {
                name: _make_greek_func(name.lower()) for name in GREEK_LABELS
            }
            fig = greeks_charts.greeks_vs_spot(greek_funcs, S, K, T, r, sigma, opt)
        st.plotly_chart(fig, use_container_width=True)

with tab_payoff:

    def _price_wrapper(S, K, T, r, sigma, option_type):
        return binom.price(S, K, T, r, sigma, N, option_type, style)

    fig = payoff_diagrams.payoff_diagram(S, K, T, r, sigma, opt, _price_wrapper)
    st.plotly_chart(fig, use_container_width=True)
