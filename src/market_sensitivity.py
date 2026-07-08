import numpy as np
import pandas as pd


def calculate_beta(portfolio_returns, benchmark_returns):
    """
    Calculates beta of a portfolio relative to a benchmark.
    """
    covariance = np.cov(portfolio_returns, benchmark_returns)[0, 1]
    benchmark_variance = np.var(benchmark_returns)

    if benchmark_variance == 0:
        return np.nan

    return covariance / benchmark_variance


def calculate_correlation(portfolio_returns, benchmark_returns):
    """
    Calculates correlation between portfolio returns and benchmark returns.
    """
    return portfolio_returns.corr(benchmark_returns)


def calculate_tracking_error(
    portfolio_returns,
    benchmark_returns,
    trading_days=252
):
    """
    Calculates annualized tracking error.
    """
    active_returns = portfolio_returns - benchmark_returns
    tracking_error = active_returns.std() * np.sqrt(trading_days)

    return tracking_error


def calculate_information_ratio(
    portfolio_returns,
    benchmark_returns,
    trading_days=252
):
    """
    Calculates Information Ratio.
    """
    active_returns = portfolio_returns - benchmark_returns

    annualized_active_return = active_returns.mean() * trading_days
    tracking_error = calculate_tracking_error(
        portfolio_returns,
        benchmark_returns,
        trading_days=trading_days
    )

    if tracking_error == 0:
        return np.nan

    return annualized_active_return / tracking_error


def calculate_upside_downside_capture(
    portfolio_returns,
    benchmark_returns
):
    """
    Calculates upside capture, downside capture, and capture ratio.
    """
    up_market_days = benchmark_returns > 0
    down_market_days = benchmark_returns < 0

    upside_capture = (
        portfolio_returns[up_market_days].mean()
        / benchmark_returns[up_market_days].mean()
    )

    downside_capture = (
        portfolio_returns[down_market_days].mean()
        / benchmark_returns[down_market_days].mean()
    )

    capture_ratio = (
        upside_capture / downside_capture
        if downside_capture != 0
        else np.nan
    )

    return {
        "Upside Capture": upside_capture,
        "Downside Capture": downside_capture,
        "Capture Ratio": capture_ratio
    }


def calculate_market_sensitivity_summary(
    portfolio_returns,
    benchmark_returns,
    trading_days=252
):
    """
    Calculates market sensitivity metrics for one or more portfolios.

    portfolio_returns can be:
    - a Series for one portfolio
    - a DataFrame for multiple portfolios
    """
    if isinstance(portfolio_returns, pd.Series):
        portfolio_returns = portfolio_returns.to_frame("Portfolio")

    results = {}

    for portfolio_name in portfolio_returns.columns:
        port_ret = portfolio_returns[portfolio_name]

        active_returns = port_ret - benchmark_returns

        beta = calculate_beta(port_ret, benchmark_returns)
        correlation = calculate_correlation(port_ret, benchmark_returns)
        tracking_error = calculate_tracking_error(
            port_ret,
            benchmark_returns,
            trading_days=trading_days
        )
        information_ratio = calculate_information_ratio(
            port_ret,
            benchmark_returns,
            trading_days=trading_days
        )

        annualized_active_return = active_returns.mean() * trading_days

        results[portfolio_name] = {
            "Beta vs Benchmark": beta,
            "Correlation vs Benchmark": correlation,
            "Annualized Active Return": annualized_active_return,
            "Tracking Error": tracking_error,
            "Information Ratio": information_ratio
        }

    return pd.DataFrame(results).T


def calculate_capture_summary(
    portfolio_returns,
    benchmark_returns
):
    """
    Calculates upside/downside capture metrics for one or more portfolios.
    """
    if isinstance(portfolio_returns, pd.Series):
        portfolio_returns = portfolio_returns.to_frame("Portfolio")

    results = {}

    for portfolio_name in portfolio_returns.columns:
        results[portfolio_name] = calculate_upside_downside_capture(
            portfolio_returns[portfolio_name],
            benchmark_returns
        )

    return pd.DataFrame(results).T


def calculate_rolling_beta(
    portfolio_returns,
    benchmark_returns,
    rolling_window=126
):
    """
    Calculates rolling beta using a rolling covariance and rolling variance.
    """
    if isinstance(portfolio_returns, pd.Series):
        portfolio_returns = portfolio_returns.to_frame("Portfolio")

    rolling_beta = pd.DataFrame(index=portfolio_returns.index)

    for portfolio_name in portfolio_returns.columns:
        rolling_covariance = portfolio_returns[portfolio_name].rolling(
            rolling_window
        ).cov(benchmark_returns)

        rolling_variance = benchmark_returns.rolling(
            rolling_window
        ).var()

        rolling_beta[portfolio_name] = rolling_covariance / rolling_variance

    return rolling_beta