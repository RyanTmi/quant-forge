"""
Provides a base class for European options contracts and concrete
subclasses for European calls and puts.
"""

from .contract import Contract

import numpy as np

from abc import abstractmethod


class EuropeanContract(Contract):
    """
    Abstract base class for European option contracts.
    """

    @abstractmethod
    def __init__(self, maturity: float, strike: float):
        """
        Initialize a European contract with a given maturity and strike price.

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


class EuropeanCall(EuropeanContract):
    """
    Concrete implementation of a European Call option.

    The payoff for a European Call is defined as:
        max(S_T - strike, 0)
    where S_T is the asset price at maturity.
    """

    def __init__(self, maturity: float, strike: float):
        super().__init__(maturity, strike)

    def payoff(self, path: np.ndarray) -> np.ndarray:
        return np.maximum(path[:, -1] - self.strike, 0)

    @property
    def name(self) -> str:
        return "European Call"


class EuropeanPut(EuropeanContract):
    """
    Concrete implementation of a European Put option.

    The payoff for a European Put is defined as:
        max(strike - S_T, 0)
    where S_T is the asset price at maturity.
    """

    def __init__(self, maturity: float, strike: float):
        super().__init__(maturity, strike)

    def payoff(self, path: np.ndarray) -> np.ndarray:
        return np.maximum(self.strike - path[:, -1], 0)

    @property
    def name(self) -> str:
        return "European Put"
