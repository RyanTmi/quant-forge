import marimo

__generated_with = "0.11.25"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""# Quant Forge: Implied Volatility Surface""")
    return


@app.cell
def _(mo):
    callout = mo.callout("""Ensure that `quant-forge` is installed using `pip install -e .`""", kind="warn")
    mo.md(f"""{callout}""")
    return (callout,)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from scipy.interpolate import griddata
    import plotly.graph_objects as go

    from quant_forge.market import get_stock_data, get_options_data, filter_options_data, plot_surface
    return (
        filter_options_data,
        get_options_data,
        get_stock_data,
        go,
        griddata,
        mo,
        np,
        plot_surface,
    )


@app.cell
def _(mo):
    symbols_options = ["AAPL", "MSFT", "TSLA", "GOOG", "JPM", "SPY"]
    symbols_options.sort()
    symbols = mo.ui.dropdown(options=symbols_options, value=symbols_options[0], full_width=True)
    return symbols, symbols_options


@app.cell(hide_code=True)
def _(mo, symbols):
    mo.md(
        rf"""Select a stock : {symbols} Fetching stock and options data for {symbols.value}. Contains the implied volality that `yfinance` gives."""
    )
    return


@app.cell
def _(get_options_data, get_stock_data, symbols):
    stock, spot_price = get_stock_data(symbols.value)
    calls_raw, _ = get_options_data(stock)
    return calls_raw, spot_price, stock


@app.cell
def _(calls_raw, filter_options_data, spot_price):
    min_strike_price = spot_price * 70 / 100
    max_strike_price = spot_price * 130 / 100

    calls = filter_options_data(calls_raw, min_strike_price, max_strike_price)
    calls
    return calls, max_strike_price, min_strike_price


@app.cell(hide_code=True)
def _(mo):
    mo.md("""Compute the implied volatility for each calls using `quant-forge` algorithms. The function `compute_implied_volatility` modify the original `DataFrame`.""")
    return


@app.cell
def _(calls):
    # Uncomment the following line to compute implied volatility using quandfor≥quand_forge.
    # compute_implied_volatility(calls, spot_price, interest_rate=0.03)
    calls
    return


app._unparsable_cell(
    r"""
    Easily plotting the implied volatility surface using the `plot_surface` function.
    """,
    name="_"
)


@app.cell
def _(calls, mo, plot_surface, spot_price):
    fig = plot_surface(calls, spot_price)
    fig.update_layout(height=700)
    mo.ui.plotly(fig)
    return (fig,)


if __name__ == "__main__":
    app.run()
