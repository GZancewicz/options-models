import functools

import numpy as np


def build_tree(S, K, T, r, sigma, N, option_type="call", exercise_style="european"):
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    p = (np.exp(r * dt) - d) / (u - d)
    american = exercise_style == "american"

    # Stock price tree (upper triangular: stock_tree[i][j] valid for i <= j)
    stock_tree = np.zeros((N + 1, N + 1))
    for j in range(N + 1):
        for i in range(j + 1):
            stock_tree[i][j] = S * (u ** (j - i)) * (d**i)

    # Option values at expiry
    option_tree = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        if option_type == "call":
            option_tree[i][N] = max(stock_tree[i][N] - K, 0)
        else:
            option_tree[i][N] = max(K - stock_tree[i][N], 0)

    # Backward induction
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            continuation = np.exp(-r * dt) * (
                p * option_tree[i][j + 1] + (1 - p) * option_tree[i + 1][j + 1]
            )
            if american:
                if option_type == "call":
                    intrinsic = max(stock_tree[i][j] - K, 0)
                else:
                    intrinsic = max(K - stock_tree[i][j], 0)
                option_tree[i][j] = max(continuation, intrinsic)
            else:
                option_tree[i][j] = continuation

    return {
        "price": option_tree[0][0],
        "stock_tree": stock_tree,
        "option_tree": option_tree,
        "u": u,
        "d": d,
        "p": p,
        "dt": dt,
    }


@functools.lru_cache(maxsize=2048)
def price(S, K, T, r, sigma, N, option_type="call", exercise_style="european"):
    return build_tree(S, K, T, r, sigma, N, option_type, exercise_style)["price"]


def greeks_finite_difference(
    S, K, T, r, sigma, N, option_type="call", exercise_style="european"
):
    h_S = S * 0.01
    h_sigma = 0.001
    h_T = 1 / 365
    h_r = 0.0001

    p0 = price(S, K, T, r, sigma, N, option_type, exercise_style)

    # Delta
    p_up = price(S + h_S, K, T, r, sigma, N, option_type, exercise_style)
    p_dn = price(S - h_S, K, T, r, sigma, N, option_type, exercise_style)
    _delta = (p_up - p_dn) / (2 * h_S)

    # Gamma
    _gamma = (p_up - 2 * p0 + p_dn) / (h_S**2)

    # Theta
    if T > h_T:
        p_later = price(S, K, T - h_T, r, sigma, N, option_type, exercise_style)
        _theta = (p_later - p0) / h_T
    else:
        _theta = 0.0

    # Vega (per 1% move)
    p_vol_up = price(S, K, T, r, sigma + h_sigma, N, option_type, exercise_style)
    p_vol_dn = price(S, K, T, r, sigma - h_sigma, N, option_type, exercise_style)
    _vega = (p_vol_up - p_vol_dn) / (2 * h_sigma) * 0.01

    # Rho (per 1% move)
    p_r_up = price(S, K, T, r + h_r, sigma, N, option_type, exercise_style)
    p_r_dn = price(S, K, T, r - h_r, sigma, N, option_type, exercise_style)
    _rho = (p_r_up - p_r_dn) / (2 * h_r) * 0.01

    return {
        "price": p0,
        "delta": _delta,
        "gamma": _gamma,
        "theta": _theta,
        "vega": _vega,
        "rho": _rho,
    }
