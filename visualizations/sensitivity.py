import numpy as np
import plotly.graph_objects as go


def price_heatmap(K, T, r, sigma, S, option_type, price_func):
    spot_range = np.linspace(S * 0.5, S * 1.5, 50)
    vol_range = np.linspace(0.05, 1.0, 50)

    Z = np.zeros((len(vol_range), len(spot_range)))
    for i, v in enumerate(vol_range):
        for j, s in enumerate(spot_range):
            Z[i][j] = price_func(s, K, T, r, v, option_type)

    fig = go.Figure(
        data=go.Heatmap(
            z=Z,
            x=np.round(spot_range, 2),
            y=np.round(vol_range, 2),
            colorscale="Viridis",
            colorbar=dict(title="Option Price"),
        )
    )
    fig.update_layout(
        title=f"{option_type.title()} Price: Underlying vs Volatility",
        xaxis_title="Underlying Asset Price",
        yaxis_title="Volatility",
        height=500,
    )
    return fig
