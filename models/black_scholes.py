import numpy as np
from scipy.stats import norm


def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


def price(S, K, T, r, sigma, option_type="call"):
    _d1 = d1(S, K, T, r, sigma)
    _d2 = d2(S, K, T, r, sigma)
    if option_type == "call":
        return S * norm.cdf(_d1) - K * np.exp(-r * T) * norm.cdf(_d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-_d2) - S * norm.cdf(-_d1)


def delta(S, K, T, r, sigma, option_type="call"):
    _d1 = d1(S, K, T, r, sigma)
    if option_type == "call":
        return norm.cdf(_d1)
    else:
        return norm.cdf(_d1) - 1.0


def gamma(S, K, T, r, sigma, option_type="call"):
    _d1 = d1(S, K, T, r, sigma)
    return norm.pdf(_d1) / (S * sigma * np.sqrt(T))


def theta(S, K, T, r, sigma, option_type="call"):
    _d1 = d1(S, K, T, r, sigma)
    _d2 = d2(S, K, T, r, sigma)
    common = -(S * norm.pdf(_d1) * sigma) / (2 * np.sqrt(T))
    if option_type == "call":
        return common - r * K * np.exp(-r * T) * norm.cdf(_d2)
    else:
        return common + r * K * np.exp(-r * T) * norm.cdf(-_d2)


def vega(S, K, T, r, sigma, option_type="call"):
    _d1 = d1(S, K, T, r, sigma)
    return S * norm.pdf(_d1) * np.sqrt(T) * 0.01


def rho(S, K, T, r, sigma, option_type="call"):
    _d2 = d2(S, K, T, r, sigma)
    if option_type == "call":
        return K * T * np.exp(-r * T) * norm.cdf(_d2) * 0.01
    else:
        return -K * T * np.exp(-r * T) * norm.cdf(-_d2) * 0.01


def all_greeks(S, K, T, r, sigma, option_type="call"):
    return {
        "price": price(S, K, T, r, sigma, option_type),
        "delta": delta(S, K, T, r, sigma, option_type),
        "gamma": gamma(S, K, T, r, sigma, option_type),
        "theta": theta(S, K, T, r, sigma, option_type),
        "vega": vega(S, K, T, r, sigma, option_type),
        "rho": rho(S, K, T, r, sigma, option_type),
    }
