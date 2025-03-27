from . import BaseModel

import numpy as np
from scipy.stats import norm

from typing import Literal


class BlackScholes(BaseModel):
    """
    Black-Scholes model for asset dynamics under constant interest rate and volatility.
    """

    def __init__(self, interest_rate: float, sigma: float):
        self._interest_rate = interest_rate
        self._sigma = sigma

    @property
    def interest_rate(self) -> float:
        return self._interest_rate

    @property
    def sigma(self) -> float:
        return self._sigma

    def drift(self, t: float, s: np.ndarray) -> np.ndarray:
        return s * self._interest_rate

    def diffusion(self, t: float, s: np.ndarray) -> np.ndarray:
        return s * self._sigma


def _d1_d2(s: float, strike: float, time_to_maturity: float, interest_rate: float, sigma: float) -> tuple[float, float]:
    d1 = (np.log(s / strike) + (interest_rate + 0.5 * sigma**2) * time_to_maturity) / (
        sigma * np.sqrt(time_to_maturity)
    )
    d2 = d1 - sigma * np.sqrt(time_to_maturity)
    return d1, d2


def black_scholes_price(
    s: float,
    strike: float,
    time_to_maturity: float,
    interest_rate: float,
    sigma: float,
    option_type: Literal["call", "put"],
) -> float:
    """
    Calculate the Black-Scholes call/put price.
    """
    d1, d2 = _d1_d2(s, strike, time_to_maturity, interest_rate, sigma)

    if option_type.lower() == "call":
        price = s * norm.cdf(d1) - strike * np.exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
    elif option_type.lower() == "put":
        price = strike * np.exp(-interest_rate * time_to_maturity) * norm.cdf(-d2) - s * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return price


def delta(
    s: float,
    strike: float,
    time_to_maturity: float,
    interest_rate: float,
    sigma: float,
    option_type: Literal["call", "put"],
) -> float:
    """
    Calculate the Delta of a European call/put option.
    """
    d1, _ = _d1_d2(s, strike, time_to_maturity, interest_rate, sigma)

    if option_type.lower() == "call":
        return norm.cdf(d1)
    elif option_type.lower() == "put":
        return norm.cdf(d1) - 1.0
    else:
        raise ValueError("option_type must be 'call' or 'put'")


def gamma(
    s: float,
    strike: float,
    time_to_maturity: float,
    interest_rate: float,
    sigma: float,
) -> float:
    """
    Calculate the Gamma of a European option (same for call and put).
    """
    d1, _ = _d1_d2(s, strike, time_to_maturity, interest_rate, sigma)
    return norm.pdf(d1) / (s * sigma * np.sqrt(time_to_maturity))


def vega(
    s: float,
    strike: float,
    time_to_maturity: float,
    interest_rate: float,
    sigma: float,
) -> float:
    """
    Calculate the Vega of a European option (same for call and put).
    """
    d1, _ = _d1_d2(s, strike, time_to_maturity, interest_rate, sigma)
    return s * np.sqrt(time_to_maturity) * norm.pdf(d1)


def theta(
    s: float,
    strike: float,
    time_to_maturity: float,
    interest_rate: float,
    sigma: float,
    option_type: Literal["call", "put"],
) -> float:
    """
    Calculate the Theta of a European call/put option.
    """
    d1, d2 = _d1_d2(s, strike, time_to_maturity, interest_rate, sigma)
    first_term = -(s * norm.pdf(d1) * sigma) / (2 * np.sqrt(time_to_maturity))

    if option_type.lower() == "call":
        second_term = -interest_rate * strike * np.exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
        return first_term + second_term
    elif option_type.lower() == "put":
        second_term = interest_rate * strike * np.exp(-interest_rate * time_to_maturity) * norm.cdf(-d2)
        return first_term + second_term
    else:
        raise ValueError("option_type must be 'call' or 'put'")


def rho(
    s: float,
    strike: float,
    time_to_maturity: float,
    interest_rate: float,
    sigma: float,
    option_type: Literal["call", "put"],
) -> float:
    """
    Calculate the Rho of a European call/put option.
    """
    _, d2 = _d1_d2(s, strike, time_to_maturity, interest_rate, sigma)

    if option_type.lower() == "call":
        return strike * time_to_maturity * np.exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
    elif option_type.lower() == "put":
        return -strike * time_to_maturity * np.exp(-interest_rate * time_to_maturity) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
