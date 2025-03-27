from .contract import Contract

import numpy as np


class Lookback(Contract):
    def __init__(self, maturity: float, vol: float):
        super().__init__(maturity)
        self.vol = vol

    def payoff(self, paths: np.ndarray) -> np.ndarray:
        """
        See https://people.maths.ox.ac.uk/gilesm/files/OPRE_2008.pdf
        """
        beta = 0.5826
        dt = self.maturity / (paths.shape[1] - 1)
        correction = 1.0 - beta * self.vol * np.sqrt(dt)
        return paths[:, -1] - np.min(paths, axis=1) * correction

    @property
    def name(self) -> str:
        return "Lookback"
