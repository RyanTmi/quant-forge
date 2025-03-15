"""
Provides a base class for Digital (binary) options and concrete
subclasses for Digital calls and puts.
"""

from .contract import Contract

import numpy as np

from abc import abstractmethod


class DigitalContract(Contract):
    """
    Abstract base class for digital (binary) options.
    """

    @abstractmethod
    def __init__(self, maturity: float, strike: float, payout: float):
        """
        Initialize a digital contract with a given maturity, strike, and fixed payout.

        Parameters
        ----------
        maturity : float
            The maturity (expiration time) of the option.
        strike : float
            The strike price at which the option can be exercised.
        payout : float
            The fixed amount paid if the option is in the money.
        """
        super().__init__(maturity)
        self._strike = strike
        self._payout = payout

    @property
    def strike(self) -> float:
        return self._strike

    @property
    def payout(self) -> float:
        return self._payout

    @abstractmethod
    def payoff(self, paths: np.ndarray) -> np.ndarray:
        pass


class DigitalCall(DigitalContract):
    """
    A digital (binary) call option. Pays out a fixed amount if S_T > strike.
    """

    def __init__(self, maturity: float, strike: float, payout: float):
        super().__init__(maturity, strike, payout)

    def payoff(self, paths: np.ndarray) -> np.ndarray:
        return self.payout * np.heaviside(paths[:, -1] - self.strike, 0)

    @property
    def name(self) -> str:
        return "Digital Call"


class DigitalPut(DigitalContract):
    """
    A digital (binary) put option. Pays out a fixed amount if S_T < strike.
    """

    def __init__(self, maturity: float, strike: float, payout: float):
        super().__init__(maturity, strike, payout)

    def payoff(self, paths: np.ndarray) -> np.ndarray:
        return self.payout * np.heaviside(self.strike - paths[:, -1], 0)

    @property
    def name(self) -> str:
        return "Digital Put"
