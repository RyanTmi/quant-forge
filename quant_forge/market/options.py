from ..calibration.implied_volatility import implied_volatility

import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata
import pandas as pd
import yfinance as yf


def get_options_data(stock: yf.Ticker) -> tuple[pd.DataFrame, pd.DataFrame]:
    calls_frames = []
    puts_frames = []

    for maturity in stock.options:
        calls = stock.option_chain(maturity).calls.copy()
        puts = stock.option_chain(maturity).puts.copy()

        columns = ["Symbol", "Expiration", "Price", "Strike", "Volume", "OpenInterest", "ImpliedVolatility", "Type"]
        for option, frames in zip([calls, puts], [calls_frames, puts_frames]):
            option["Symbol"] = stock.ticker
            option["Expiration"] = maturity
            option["Type"] = "Call" if option is calls else "Put"

            option = option.rename(
                columns={
                    "lastPrice": "Price",
                    "impliedVolatility": "ImpliedVolatility",
                    "volume": "Volume",
                    "openInterest": "OpenInterest",
                    "strike": "Strike",
                }
            )
            frames.append(option[columns])

    calls = pd.concat(calls_frames, ignore_index=True).dropna().reset_index(drop=True)
    puts = pd.concat(puts_frames, ignore_index=True).dropna().reset_index(drop=True)
    return calls, puts


def filter_options_data(options_data: pd.DataFrame, min_strike_price: float, max_strike_price: float) -> pd.DataFrame:
    # Strike price filter
    strike_price_mask = (options_data["Strike"] >= min_strike_price) & (options_data["Strike"] <= max_strike_price)
    filtered_options_data = options_data[strike_price_mask]

    # Time to maturity filter
    time_to_maturity = (pd.to_datetime(filtered_options_data["Expiration"]) - pd.Timestamp.today()).dt.days / 365
    filtered_options_data = filtered_options_data[time_to_maturity >= 0.07]

    # Open interest filter
    # filtered_options_data = filtered_options_data[filtered_options_data["OpenInterest"] >= 100]

    filtered_options_data.reset_index(drop=True, inplace=True)
    return filtered_options_data


def get_options_surface_data(options_data: pd.DataFrame) -> pd.DataFrame:
    surface_data = options_data.copy()
    surface_data["TimeToMaturity"] = (pd.to_datetime(surface_data["Expiration"]) - pd.Timestamp.today()).dt.days / 365
    surface_data = surface_data[["Strike", "ImpliedVolatility", "TimeToMaturity"]]
    return surface_data


def compute_implied_volatility(options_data: pd.DataFrame, spot_price: float, interest_rate: float) -> None:
    ivs = np.zeros(len(options_data))
    option_type = options_data["Type"].iloc[0].lower()
    for i, row in enumerate(options_data["Price"]):
        ivs[i] = implied_volatility(
            row,
            spot_price,
            options_data["Strike"].iloc[i],
            (pd.to_datetime(options_data["Expiration"].iloc[i]) - pd.Timestamp.today()).days / 365,
            interest_rate,
            option_type,
        )
    options_data["ImpliedVolatility"] = ivs
    options_data.dropna(inplace=True)
    options_data.reset_index(drop=True, inplace=True)


def plot_surface(options_data: pd.DataFrame, spot_price: float) -> go.Figure:
    symbol = options_data["Symbol"].iloc[0]
    options_surface_data = get_options_surface_data(options_data)

    moneyness = options_surface_data["Strike"] / spot_price
    time_to_maturity = options_surface_data["TimeToMaturity"]
    implied_volatility = options_surface_data["ImpliedVolatility"] * 100

    x = np.linspace(moneyness.min(), moneyness.max(), 30)
    y = np.linspace(time_to_maturity.min(), time_to_maturity.max(), 30)
    x, y = np.meshgrid(x, y)
    z = griddata((moneyness, time_to_maturity), implied_volatility, (x, y), method="linear")

    fig = go.Figure(data=go.Surface(x=x, y=y, z=z, colorscale="Viridis", showscale=False))
    fig.update_layout(
        title=f"Implied Volatility Surface for {symbol}",
        scene=dict(
            xaxis_title="Moneyness", yaxis_title="Time to Maturity (years)", zaxis_title="Implied Volatility (%)"
        ),
    )
    return fig
