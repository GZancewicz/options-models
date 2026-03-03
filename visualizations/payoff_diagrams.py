import numpy as np
import plotly.graph_objects as go


def payoff_diagram(S, K, T, r, sigma, option_type, price_func):
    spot_range = np.linspace(K * 0.5, K * 1.5, 200)

    if option_type == "call":
        intrinsic = np.maximum(spot_range - K, 0)
    else:
        intrinsic = np.maximum(K - spot_range, 0)

    current_value = np.array(
        [price_func(s, K, T, r, sigma, option_type) for s in spot_range]
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=spot_range,
            y=intrinsic,
            name="Payoff at Expiry",
            line=dict(dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=spot_range,
            y=current_value,
            name="Current Value",
            line=dict(width=2),
        )
    )

    # Combine label when Strike and Spot are at the same price
    if abs(S - K) < (K * 0.01):
        fig.add_vline(
            x=K, line_dash="dash", line_color="red",
            annotation_text="Strike / Spot",
        )
    else:
        fig.add_vline(x=K, line_dash="dot", annotation_text="Strike")
        fig.add_vline(
            x=S, line_dash="dash", line_color="red", annotation_text="Spot",
        )

    fig.update_layout(
        title=f"{option_type.title()} Option Payoff",
        xaxis_title="Underlying Asset Price",
        yaxis_title="Option Value",
        height=400,
    )
    return fig


def binary_payoff_diagram(S, K, T, r, sigma, option_type, price_func):
    """Payoff diagram for a binary/digital option (step function, not hockey stick)."""
    spot_range = np.linspace(K * 0.5, K * 1.5, 500)

    # Binary payoff at expiry: step function
    if option_type == "call":
        intrinsic = np.where(spot_range > K, 1.0, 0.0)
    else:
        intrinsic = np.where(spot_range < K, 1.0, 0.0)

    current_value = np.array(
        [price_func(s, K, T, r, sigma, option_type) for s in spot_range]
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=spot_range,
            y=intrinsic,
            name="Payoff at Expiry",
            line=dict(dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=spot_range,
            y=current_value,
            name="Current Value",
            line=dict(width=2),
        )
    )

    if abs(S - K) < (K * 0.01):
        fig.add_vline(
            x=K, line_dash="dash", line_color="red",
            annotation_text="Strike / Spot",
        )
    else:
        fig.add_vline(x=K, line_dash="dot", annotation_text="Strike")
        fig.add_vline(
            x=S, line_dash="dash", line_color="red", annotation_text="Spot",
        )

    fig.update_layout(
        title=f"Binary {option_type.title()} Payoff",
        xaxis_title="Underlying Asset Price",
        yaxis_title="Option Value",
        height=400,
    )
    return fig


def spread_payoff_diagram(S, K_call, K_put, T, r, sigma, price_func):
    """Payoff diagram for a binary spread (call at K_call + put at K_put)."""
    lo = min(K_put, K_call) * 0.6
    hi = max(K_put, K_call) * 1.4
    spot_range = np.linspace(lo, hi, 300)

    call_values = np.array(
        [price_func(s, K_call, T, r, sigma, "call") for s in spot_range]
    )
    put_values = np.array(
        [price_func(s, K_put, T, r, sigma, "put") for s in spot_range]
    )
    combined = call_values + put_values

    # Intrinsic payoff at expiry
    call_intrinsic = np.where(spot_range > K_call, 1.0, 0.0)
    put_intrinsic = np.where(spot_range < K_put, 1.0, 0.0)
    combined_intrinsic = call_intrinsic + put_intrinsic

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=spot_range,
            y=combined_intrinsic,
            name="Combined Payoff at Expiry",
            line=dict(dash="dash", color="gray"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=spot_range,
            y=call_values,
            name=f"Binary Call (K={K_call})",
            line=dict(width=1.5, dash="dot"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=spot_range,
            y=put_values,
            name=f"Binary Put (K={K_put})",
            line=dict(width=1.5, dash="dot"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=spot_range,
            y=combined,
            name="Combined Value",
            line=dict(width=3),
        )
    )

    fig.add_vline(x=K_call, line_dash="dot", annotation_text=f"Call Strike ({K_call})")
    fig.add_vline(x=K_put, line_dash="dot", annotation_text=f"Put Strike ({K_put})",
                  annotation_position="bottom right")
    fig.add_vline(x=S, line_dash="dash", line_color="red", annotation_text="Spot")

    fig.update_layout(
        title="Binary Spread Payoff",
        xaxis_title="Underlying Asset Price",
        yaxis_title="Option Value",
        height=500,
    )
    return fig
