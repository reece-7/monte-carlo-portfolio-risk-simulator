import numpy as np
import pandas as pd


def calculate_portfolio_returns(returns, weights):
    """
    Calculates daily portfolio returns from asset returns and portfolio weights.
    """
    weights = pd.Series(weights)
    weights = weights[returns.columns]

    portfolio_returns = returns @ weights.values

    return portfolio_returns


def calculate_cumulative_values(
    portfolio_returns,
    initial_value=10_000
):
    """
    Calculates cumulative portfolio value over time.
    """
    cumulative_values = initial_value * (1 + portfolio_returns).cumprod()

    return cumulative_values


def calculate_annualized_return(
    portfolio_returns,
    trading_days=252
):
    """
    Calculates annualized return from daily returns.
    """
    annualized_return = portfolio_returns.mean() * trading_days

    return annualized_return


def calculate_annualized_volatility(
    portfolio_returns,
    trading_days=252
):
    """
    Calculates annualized volatility from daily returns.
    """
    annualized_volatility = portfolio_returns.std() * np.sqrt(trading_days)

    return annualized_volatility


def calculate_sharpe_ratio(
    annualized_return,
    annualized_volatility,
    risk_free_rate=0.00
):
    """
    Calculates Sharpe Ratio.
    """
    if annualized_volatility == 0:
        return np.nan

    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility

    return sharpe_ratio


def calculate_drawdowns(portfolio_values):
    """
    Calculates drawdowns from portfolio value series.
    """
    running_max = portfolio_values.cummax()
    drawdowns = portfolio_values / running_max - 1

    return drawdowns


def calculate_max_drawdown(portfolio_values):
    """
    Calculates maximum drawdown.
    """
    drawdowns = calculate_drawdowns(portfolio_values)
    max_drawdown = drawdowns.min()

    return max_drawdown


def calculate_var(
    returns,
    confidence_level=0.95
):
    """
    Calculates historical Value at Risk.
    """
    percentile = (1 - confidence_level) * 100
    value_at_risk = np.percentile(returns, percentile)

    return value_at_risk


def calculate_expected_shortfall(
    returns,
    confidence_level=0.95
):
    """
    Calculates historical Expected Shortfall.
    """
    var = calculate_var(returns, confidence_level)
    expected_shortfall = returns[returns <= var].mean()

    return expected_shortfall


def calculate_performance_summary(
    portfolio_returns,
    initial_value=10_000,
    trading_days=252,
    risk_free_rate=0.00,
    confidence_level=0.95
):
    """
    Calculates a complete performance and risk summary.
    """
    portfolio_values = calculate_cumulative_values(
        portfolio_returns,
        initial_value=initial_value
    )

    final_value = portfolio_values.iloc[-1]
    total_return = final_value / portfolio_values.iloc[0] - 1

    annualized_return = calculate_annualized_return(
        portfolio_returns,
        trading_days=trading_days
    )

    annualized_volatility = calculate_annualized_volatility(
        portfolio_returns,
        trading_days=trading_days
    )

    sharpe_ratio = calculate_sharpe_ratio(
        annualized_return,
        annualized_volatility,
        risk_free_rate=risk_free_rate
    )

    max_drawdown = calculate_max_drawdown(portfolio_values)

    var_95 = calculate_var(
        portfolio_returns,
        confidence_level=confidence_level
    )

    expected_shortfall_95 = calculate_expected_shortfall(
        portfolio_returns,
        confidence_level=confidence_level
    )

    summary = {
        "Final Value": final_value,
        "Total Return": total_return,
        "Annualized Return": annualized_return,
        "Annualized Volatility": annualized_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Maximum Drawdown": max_drawdown,
        "Historical VaR 95%": var_95,
        "Historical Expected Shortfall 95%": expected_shortfall_95
    }

    return summary