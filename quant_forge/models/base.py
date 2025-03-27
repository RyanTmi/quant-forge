"""
Defines an abstract base class for financial models representing asset dynamics.
This class enforces the implementation of drift and diffusion methods which are
used by simulation engines for numerical integration of stochastic differential equations.
"""

import numpy as np

from abc import ABC, abstractmethod


class BaseModel(ABC):
    """
    Abstract base class for financial models representing asset price dynamics.

    This class defines the interface for the model's dynamics by requiring the implementation
    of the drift and diffusion functions. These functions describe the deterministic (drift) and
    stochastic (diffusion) components of the asset's evolution over time.
    """

    @abstractmethod
    def drift(self, t: float, s: np.ndarray) -> np.ndarray:
        """
        Compute the drift coefficient of the asset price process.

        Parameters
        ----------
        t : float
            Current time.
        s : np.ndarray
            Current asset price.

        Returns
        -------
        np.ndarray
            The drift coefficient.
        """
        pass

    @abstractmethod
    def diffusion(self, t: float, s: np.ndarray) -> np.ndarray:
        """
        Compute the diffusion coefficient of the asset price process.

        Parameters
        ----------
        t : float
            Current time.
        s : np.ndarray
            Current asset price.

        Returns
        -------
        np.ndarray
            The diffusion coefficient.
        """
        pass
