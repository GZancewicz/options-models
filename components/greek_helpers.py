import streamlit as st

GREEK_LABELS = ["Price", "Delta", "Gamma", "Theta", "Vega", "Rho"]

GREEK_HELP = {
    "Price": "Theoretical fair value of the option under the model's assumptions.",
    "Delta": "Rate of change of option price per $1 move in the underlying. "
    "Ranges from 0 to 1 for calls, -1 to 0 for puts.",
    "Gamma": "Rate of change of Delta per $1 move in the underlying. "
    "Measures the curvature of the option's price curve.",
    "Theta": "Rate of time decay — how much value the option loses per day, "
    "all else equal. Typically negative (options lose value over time).",
    "Vega": "Sensitivity to a 1% change in implied volatility. "
    "Higher Vega means the option is more sensitive to volatility changes.",
    "Rho": "Sensitivity to a 1% change in the risk-free interest rate. "
    "Calls gain value when rates rise; puts lose value.",
}

BINARY_GREEK_HELP = {
    "Price": "Probability-weighted present value of the payout. "
    "Represents the fair price of the binary option.",
    "Delta": "Rate of change of option price per $1 move in the underlying. "
    "Can spike sharply near the strike as expiry approaches.",
    "Gamma": "Rate of change of Delta per $1 move in the underlying. "
    "Binary options have extreme Gamma near the strike.",
    "Theta": "Rate of time decay — how much value the option loses per day. "
    "Can be positive or negative for binary options depending on moneyness.",
    "Vega": "Sensitivity to a 1% change in implied volatility. "
    "Unlike vanilla options, binary Vega can be negative.",
    "Rho": "Sensitivity to a 1% change in the risk-free interest rate.",
}


def show_greek_metrics(results, show_greeks, help_dict=None):
    """Display price (always) and optionally all Greek metrics in a row."""
    if help_dict is None:
        help_dict = GREEK_HELP
    if show_greeks:
        cols = st.columns(6)
        for col, label in zip(cols, GREEK_LABELS):
            col.metric(label, f"{results[label.lower()]:.4f}", help=help_dict[label])
    else:
        st.metric("Price", f"{results['price']:.4f}", help=help_dict["Price"])


CUSTOM_CSS = """
<style>
    /* Hide the deploy button only */
    .stDeployButton {display: none !important;}
    [data-testid="stAppDeployButton"] {display: none !important;}

    /* Style the main menu button as a gear */
    [data-testid="stMainMenu"] > button::before {
        content: "\\2699";
        font-size: 1.4rem;
    }
    [data-testid="stMainMenu"] > button > svg {
        display: none;
    }
</style>
"""


def inject_custom_css():
    """Inject CSS to hide the deploy button and restyle the menu as a gear."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
