"""
Provides a simulation engine for generating asset price paths using a specified
numerical scheme. This engine takes a financial model (with defined drift and diffusion)
and simulates paths accordingly.
"""

from ..models import BaseModel, BlackScholes

import numpy as np

from typing import Literal


class PathSimulator:
    """
    A simulation engine for generating asset price paths from a given financial model.
    """

    def __init__(self, model: BaseModel):
        """
        Initialize the simulator with a financial model.

        Parameters
        ----------
        model : BaseModel
            A financial model with defined drift and diffusion functions.
        """
        self.model = model

    def simulate(
        self,
        s0: float,
        t1: float,
        n_steps: int,
        n_paths: int,
        *,
        scheme: Literal["euler", "exact"] = "euler",
    ) -> np.ndarray:
        """
        Simulate asset price paths using the provided model dynamics and numerical scheme.

        Parameters
        ----------
        s0 : float
            Initial asset price.
        t1 : float
            Total simulation time.
        n_steps : int
            Number of time steps.
        n_paths : int
            Number of simulation paths.
        scheme : str, optional
            Simulation scheme to use, by default "euler"

        Returns
        -------
        np.ndarray
            An array of simulated asset price paths.
        """
        dt = t1 / n_steps
        paths = np.empty((n_paths, n_steps + 1, 1))
        paths[:, 0] = s0
        dw = np.random.normal(scale=np.sqrt(dt), size=(n_paths, n_steps, 1))

        if scheme.lower() == "euler":
            for i in range(n_steps):
                drift = self.model.drift(i * dt, paths[:, i])
                diffusion = self.model.diffusion(i * dt, paths[:, i])
                paths[:, i + 1] = paths[:, i] + drift * dt + diffusion * dw[:, i]
        elif scheme.lower() == "exact":
            if isinstance(self.model, BlackScholes):
                mu = self.model.interest_rate
                sigma = self.model.sigma
                paths[:, 1:] = s0 * np.cumprod(np.exp((mu - sigma**2 / 2) * dt + sigma * dw), axis=1)
            else:
                raise ValueError(f"Model is not exactly simulable")
        else:
            raise ValueError(f"Unknown simulation scheme: {scheme}")

        return paths
