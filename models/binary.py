import numpy as np
from scipy.stats import norm


def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


def price(S, K, T, r, sigma, option_type="call"):
    """Cash-or-nothing binary option that pays a fixed amount if in the money at expiry."""
    _d2 = d2(S, K, T, r, sigma)
    if option_type == "call":
        return np.exp(-r * T) * norm.cdf(_d2)
    else:
        return np.exp(-r * T) * norm.cdf(-_d2)


def delta(S, K, T, r, sigma, option_type="call"):
    _d2 = d2(S, K, T, r, sigma)
    coeff = np.exp(-r * T) / (S * sigma * np.sqrt(T))
    if option_type == "call":
        return coeff * norm.pdf(_d2)
    else:
        return -coeff * norm.pdf(-_d2)


def gamma(S, K, T, r, sigma, option_type="call"):
    _d1 = d1(S, K, T, r, sigma)
    _d2 = d2(S, K, T, r, sigma)
    coeff = np.exp(-r * T) / (S**2 * sigma**2 * T)
    if option_type == "call":
        return -coeff * norm.pdf(_d2) * _d1
    else:
        return coeff * norm.pdf(-_d2) * _d1


def theta(S, K, T, r, sigma, option_type="call"):
    """Theta via finite difference (analytical form is complex for binaries)."""
    h = 1 / 365
    if T > h:
        return (price(S, K, T - h, r, sigma, option_type)
                - price(S, K, T, r, sigma, option_type)) / h
    return 0.0


def vega(S, K, T, r, sigma, option_type="call"):
    """Vega per 1% move in volatility."""
    h = 0.001
    p_up = price(S, K, T, r, sigma + h, option_type)
    p_dn = price(S, K, T, r, sigma - h, option_type)
    return (p_up - p_dn) / (2 * h) * 0.01


def rho(S, K, T, r, sigma, option_type="call"):
    """Rho per 1% move in rate."""
    h = 0.0001
    p_up = price(S, K, T, r + h, sigma, option_type)
    p_dn = price(S, K, T, r - h, sigma, option_type)
    return (p_up - p_dn) / (2 * h) * 0.01


def all_greeks(S, K, T, r, sigma, option_type="call"):
    return {
        "price": price(S, K, T, r, sigma, option_type),
        "delta": delta(S, K, T, r, sigma, option_type),
        "gamma": gamma(S, K, T, r, sigma, option_type),
        "theta": theta(S, K, T, r, sigma, option_type),
        "vega": vega(S, K, T, r, sigma, option_type),
        "rho": rho(S, K, T, r, sigma, option_type),
    }
