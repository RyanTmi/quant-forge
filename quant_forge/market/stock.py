import yfinance as yf


def get_stock_data(symbol: str) -> tuple[yf.Ticker, float]:
    stock = yf.Ticker(symbol)
    spot_price = stock.history()["Close"].iloc[-1]

    return stock, spot_price
