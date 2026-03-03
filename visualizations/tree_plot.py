import plotly.graph_objects as go


def binomial_tree_figure(stock_tree, option_tree, N, max_display_steps=15):
    display_N = min(N, max_display_steps)

    node_x, node_y = [], []
    node_text = []
    edge_x, edge_y = [], []

    for j in range(display_N + 1):
        for i in range(j + 1):
            x = j
            y = j - 2 * i
            node_x.append(x)
            node_y.append(y)
            node_text.append(
                f"Asset={stock_tree[i][j]:.2f}<br>Value={option_tree[i][j]:.2f}"
            )

            if j < display_N:
                # Up child: (i, j+1)
                child_up_y = (j + 1) - 2 * i
                edge_x.extend([x, j + 1, None])
                edge_y.extend([y, child_up_y, None])
                # Down child: (i+1, j+1)
                child_dn_y = (j + 1) - 2 * (i + 1)
                edge_x.extend([x, j + 1, None])
                edge_y.extend([y, child_dn_y, None])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(color="lightgray", width=1),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            marker=dict(size=10, color="steelblue"),
            text=node_text,
            hoverinfo="text",
            showlegend=False,
        )
    )

    fig.update_layout(
        title=f"Binomial Tree (showing {display_N} of {N} steps)",
        xaxis_title="Time Step",
        yaxis=dict(visible=False),
        height=max(400, display_N * 50),
        showlegend=False,
    )
    fig.update_xaxes(dtick=1)
    return fig
