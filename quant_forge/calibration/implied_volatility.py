"""
Implements implied volatility calculations for option pricing,
particularly using the Newton-Raphson method for inverting the Black-Scholes formula.
"""

from ..models.black_scholes import black_scholes_price, vega

import numpy as np

from typing import Literal


def implied_volatility(
    market_price: float,
    s: float,
    strike: float,
    time_to_maturity: float,
    interest_rate: float,
    option_type: Literal["call", "put"],
) -> float:
    """
    Calculate the implied volatility using the Newton-Raphson method.

    Parameters
    ----------
    market_price : float
        Market price of the option.
    s : float
        Current asset price.
    strike : float
        Strike price.
    time_to_maturity : float
        Time to maturity.
    interest_rate : float
        Risk-free interest rate.
    option_type : Literal['call', 'put']
        The options type.

    Returns
    -------
    float
        The implied volatility.
    """
    max_iterations = 200
    tol = 1e-5
    iv = 0.3

    for _ in range(max_iterations):
        bs_price = black_scholes_price(s, strike, time_to_maturity, interest_rate, iv, option_type)
        vg = vega(s, strike, time_to_maturity, interest_rate, iv)
        if vg == 0:
            return np.nan

        diff = bs_price - market_price
        iv_new = iv - diff / vg
        if iv_new < 0 or iv_new > 2:
            return np.nan

        bs_price_new = black_scholes_price(s, strike, time_to_maturity, interest_rate, iv_new, option_type)
        if np.abs(iv - iv_new) < tol or np.abs(bs_price_new - market_price) < tol or vg < tol:
            break

        iv = iv_new

    return iv
