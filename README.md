# Quant Forge

**Quant Forge** is an open-source Python library under active development for quantitative finance. The project’s vision is to build a flexible and modular toolkit for pricing, simulation, calibration, and visualization of financial instruments.

## Current Features

- **Models**:  
  The package currently implements a robust Black–Scholes model. This includes:
  - A BlackScholes class that defines the asset dynamics through drift and diffusion functions, making it compatible with the simulation engine.
  - Greeks calculation under the Black–Scholes framework: delta, gamma, vega, theta, rho.
  
- **Simulations**:  
  Provides a basic path simulation engine supporting Euler and exact simulation schemes.
  
- **Contracts**:  
  Offers various derivative contracts including European, Asian, Digital, and Lookback options.
  
- **Calibration**:  
  Includes an implied volatility calculator using the Newton–Raphson method.

## Future Goals

Quant Forge aims to expand its capabilities by adding:

- **Advanced Pricing Methods**:  
  Closed-form formulas, FFT-based pricing, Monte Carlo simulations, and finite difference solvers.
  
- **Extended Models**:  
  Stochastic volatility, local volatility, and other advanced financial models.
  
- **Enhanced Simulation Tools**:  
  Higher-order numerical schemes, variance reduction techniques, and parallel/distributed simulation support.
  
- **Visualization Tools**:  
  Comprehensive plotting and analysis of pricing surfaces, risk measures, and model calibration.

## Examples

The [examples/](examples/) directory contains example notebooks demonstrating how to use Quant Forge.

- [volatility_surface](examples/volatility_surface.ipynb) notebook shows how to generate and plot an implied volatility surface for a given stock.

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/RyanTmi/quant-forge.git
cd quant-forge
pip install -e .
```

## License

Quant Forge is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions, suggestions, or feedback, please open an issue on GitHub or contact the maintainers at <timeusryan@gmail.com>.
