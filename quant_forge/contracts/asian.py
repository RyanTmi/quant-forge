"""
Provides a base class for Asian options contracts and concrete
subclasses for Asian calls and puts.
"""

from .contract import Contract

import numpy as np

from abc import abstractmethod


class AsianContract(Contract):
    @abstractmethod
    def __init__(self, maturity: float, strike: float):
        """
        Initialize a Asian contract with a given maturity and strike price.

        Parameters
        ----------
        maturity : float
            The maturity (expiration time) of the option.
        strike : float
            The strike price at which the option can be exercised.
        """
        super().__init__(maturity)
        self._strike = strike

    @property
    def strike(self) -> float:
        return self._strike


class AsianCall(AsianContract):
    """
    An Asian call option.
    """

    def __init__(self, maturity: float, strike: float) -> None:
        super().__init__(maturity, strike)

    def payoff(self, paths: np.ndarray) -> np.ndarray:
        dt = self.maturity / (paths.shape[1] - 1)
        s = dt * np.sum(paths[:, 1:] + paths[:, :-1], axis=1) / 2
        return np.maximum(s - self.strike, 0)

    @property
    def name(self) -> str:
        return "Asian Call"


class AsianPut(AsianContract):
    """
    An Asian put option.
    """

    def __init__(self, maturity: float, strike: float) -> None:
        super().__init__(maturity, strike)

    def payoff(self, paths: np.ndarray) -> np.ndarray:
        dt = self.maturity / (paths.shape[1] - 1)
        s = dt * np.sum(paths[:, 1:] + paths[:, :-1], axis=1) / 2
        return np.maximum(self.strike - s, 0)

    @property
    def name(self) -> str:
        return "Asian Put"
