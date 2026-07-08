from pathlib import Path

import pandas as pd
import yfinance as yf


def download_price_data(
    tickers,
    start_date="2018-01-01",
    end_date=None,
    auto_adjust=True
):
    """
    Downloads historical closing prices from Yahoo Finance.

    Raises a clear ValueError if tickers are missing, invalid,
    or if not enough price data is available.
    """
    tickers = [ticker.upper().strip() for ticker in tickers if ticker.strip() != ""]

    if len(tickers) == 0:
        raise ValueError("No valid tickers were provided.")

    raw_data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        auto_adjust=auto_adjust,
        progress=False
    )

    if raw_data.empty:
        raise ValueError(
            "No price data was downloaded. Please check your tickers, date range, and internet connection."
        )

    if isinstance(raw_data.columns, pd.MultiIndex):
        if "Close" in raw_data.columns.get_level_values(0):
            prices = raw_data["Close"]
        elif "Adj Close" in raw_data.columns.get_level_values(0):
            prices = raw_data["Adj Close"]
        else:
            raise ValueError("No closing price data was found for the selected tickers.")
    else:
        if "Close" in raw_data.columns:
            prices = raw_data["Close"]
        elif "Adj Close" in raw_data.columns:
            prices = raw_data["Adj Close"]
        else:
            raise ValueError("No closing price data was found for the selected ticker.")

    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    prices = prices.dropna(axis=1, how="all")

    missing_tickers = [
        ticker for ticker in tickers
        if ticker not in prices.columns
    ]

    if missing_tickers:
        raise ValueError(
            f"The following tickers could not be downloaded or have no price data: {missing_tickers}"
        )

    prices = prices.dropna()

    if len(prices) < 60:
        raise ValueError(
            "Not enough historical data is available. Please choose an earlier start date or different tickers."
        )

    return prices


def calculate_daily_returns(prices):
    """
    Calculates daily percentage returns from a price DataFrame.
    """
    returns = prices.pct_change().dropna()
    return returns


def load_returns(filepath):
    """
    Loads daily returns from a CSV file.
    """
    filepath = Path(filepath)

    returns = pd.read_csv(
        filepath,
        index_col=0,
        parse_dates=True
    )

    return returns


def save_dataframe(dataframe, filepath):
    """
    Saves a DataFrame to CSV.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(filepath)


def validate_weights(weights, expected_assets):
    """
    Validates that portfolio weights match the expected assets and sum to 1.
    """
    weights = pd.Series(weights)

    missing_assets = set(expected_assets) - set(weights.index)
    extra_assets = set(weights.index) - set(expected_assets)

    if missing_assets:
        raise ValueError(f"Missing weights for assets: {missing_assets}")

    if extra_assets:
        raise ValueError(f"Unexpected assets in weights: {extra_assets}")

    weights = weights[expected_assets]

    if abs(weights.sum() - 1.0) > 1e-6:
        raise ValueError("Portfolio weights must sum to 1.0")

    return weights