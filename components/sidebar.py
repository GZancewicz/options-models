import streamlit as st

DEFAULTS = {
    "S": 75.0,
    "K": 75.0,
    "T_weeks": 52,
    "sigma": 0.20,
    "r": 0.05,
    "N": 50,
}


def render_sidebar(show_steps=False, show_exercise_style=False):
    st.sidebar.header("Option Parameters")

    if st.sidebar.button("Reset to Defaults"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    option_type = st.sidebar.radio("Option Type", ["Call", "Put"], horizontal=True)

    exercise_style = "european"
    if show_exercise_style:
        exercise_style = st.sidebar.radio(
            "Exercise Style", ["American", "European"], horizontal=True
        ).lower()

    S = st.sidebar.number_input(
        "Underlying Asset Price (S)", min_value=1.0, value=DEFAULTS["S"], step=1.0
    )
    K = st.sidebar.number_input(
        "Strike (K)", min_value=1.0, value=DEFAULTS["K"], step=1.0
    )
    T_weeks = st.sidebar.slider(
        "Time to Expiry (weeks)",
        min_value=1,
        max_value=156,
        value=DEFAULTS["T_weeks"],
        step=1,
    )
    T = T_weeks / 52.0
    sigma = st.sidebar.slider(
        "Volatility (σ)",
        min_value=0.01,
        max_value=1.50,
        value=DEFAULTS["sigma"],
        step=0.01,
    )
    r = st.sidebar.slider(
        "Risk-Free Rate (r)",
        min_value=0.0,
        max_value=0.20,
        value=DEFAULTS["r"],
        step=0.005,
    )

    params = {
        "S": S,
        "K": K,
        "T": T,
        "sigma": sigma,
        "r": r,
        "option_type": option_type.lower(),
        "exercise_style": exercise_style,
    }

    if show_steps:
        N = st.sidebar.slider(
            "Binomial Steps (N)",
            min_value=1,
            max_value=200,
            value=DEFAULTS["N"],
            step=1,
        )
        params["N"] = N

    return params
