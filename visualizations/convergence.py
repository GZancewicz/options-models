import numpy as np
import plotly.graph_objects as go

from models import black_scholes, binomial


def convergence_chart(S, K, T, r, sigma, option_type, max_steps=200):
    bs_price = black_scholes.price(S, K, T, r, sigma, option_type)

    steps = np.arange(1, max_steps + 1)
    bin_prices = np.array(
        [binomial.price(S, K, T, r, sigma, n, option_type) for n in steps]
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=steps, y=bin_prices, name="Binomial Price", mode="lines")
    )
    fig.add_hline(
        y=bs_price,
        line_dash="dash",
        line_color="red",
        annotation_text=f"BS = {bs_price:.4f}",
    )
    fig.update_layout(
        title="Binomial Convergence to Black-Scholes",
        xaxis_title="Number of Steps",
        yaxis_title="Option Price",
        height=500,
    )
    return fig
