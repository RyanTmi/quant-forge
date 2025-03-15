import numpy as np

from abc import ABC, abstractmethod


class Contract(ABC):
    def __init__(self, maturity: float):
        self._maturity = maturity

    @property
    def maturity(self) -> float:
        return self._maturity

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def payoff(self, paths: np.ndarray) -> np.ndarray:
        pass
