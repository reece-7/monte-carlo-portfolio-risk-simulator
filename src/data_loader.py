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
    Downloads historical adjusted close prices for a list of tickers.
    """
    prices = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=auto_adjust,
        progress=False
    )["Close"]

    if isinstance(prices, pd.Series):
        prices = prices.to_frame()

    prices = prices.dropna()

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