import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def greeks_vs_spot(greek_func_map, S, K, T, r, sigma, option_type):
    spot_range = np.linspace(S * 0.5, S * 1.5, 200)

    names = list(greek_func_map.keys())
    fig = make_subplots(
        rows=3,
        cols=2,
        subplot_titles=names,
        vertical_spacing=0.12,
        horizontal_spacing=0.10,
    )

    for idx, (name, func) in enumerate(greek_func_map.items()):
        row = idx // 2 + 1
        col = idx % 2 + 1
        values = func(spot_range, K, T, r, sigma, option_type)
        fig.add_trace(
            go.Scatter(x=spot_range, y=values, name=name, line=dict(width=2)),
            row=row,
            col=col,
        )
        fig.add_vline(x=S, line_dash="dash", line_color="gray", row=row, col=col)

    # Label all x-axes
    for i in range(1, 7):
        fig.update_xaxes(title_text="Underlying Asset Price", row=(i - 1) // 2 + 1, col=(i - 1) % 2 + 1)

    fig.update_layout(
        height=900,
        showlegend=False,
        title_text=f"Greeks vs Underlying Asset Price ({option_type.title()})",
        margin=dict(b=40),
    )
    return fig
