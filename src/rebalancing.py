import numpy as np
import pandas as pd


def get_rebalance_dates(returns_index, frequency):
    """
    Returns the last available trading day for each rebalancing period.

    frequency:
    - "M" monthly
    - "Q" quarterly
    - "Y" annual
    """
    return returns_index.to_series().groupby(
        returns_index.to_period(frequency)
    ).tail(1).index


def simulate_rebalanced_portfolio(
    returns,
    weights,
    initial_value=10_000,
    rebalance_frequency=None
):
    """
    Simulates portfolio value over time.

    If rebalance_frequency is None, the strategy is Buy & Hold.
    Otherwise, the portfolio is rebalanced at the selected frequency.
    """
    weights = pd.Series(weights)
    weights = weights[returns.columns]

    asset_values = weights * initial_value
    portfolio_values = []

    if rebalance_frequency is not None:
        rebalance_dates = set(
            get_rebalance_dates(returns.index, rebalance_frequency)
        )
    else:
        rebalance_dates = set()

    for date, daily_return in returns.iterrows():
        asset_values = asset_values * (1 + daily_return)

        total_value = asset_values.sum()
        portfolio_values.append(total_value)

        if date in rebalance_dates:
            asset_values = weights * total_value

    return pd.Series(
        portfolio_values,
        index=returns.index,
        name="Portfolio Value"
    )


def simulate_rebalanced_portfolio_with_costs(
    returns,
    weights,
    initial_value=10_000,
    rebalance_frequency=None,
    transaction_cost_rate=0.00
):
    """
    Simulates portfolio value over time with optional rebalancing and transaction costs.

    transaction_cost_rate example:
    0.001 = 0.10% per dollar traded.
    """
    weights = pd.Series(weights)
    weights = weights[returns.columns]

    asset_values = weights * initial_value
    portfolio_values = []
    transaction_costs = []

    if rebalance_frequency is not None:
        rebalance_dates = set(
            get_rebalance_dates(returns.index, rebalance_frequency)
        )
    else:
        rebalance_dates = set()

    for date, daily_return in returns.iterrows():
        asset_values = asset_values * (1 + daily_return)
        daily_transaction_cost = 0.00

        if date in rebalance_dates:
            total_value_before_cost = asset_values.sum()
            target_asset_values = weights * total_value_before_cost

            trades = target_asset_values - asset_values
            dollar_turnover = trades.abs().sum()

            daily_transaction_cost = dollar_turnover * transaction_cost_rate

            total_value_after_cost = total_value_before_cost - daily_transaction_cost
            asset_values = weights * total_value_after_cost

        portfolio_values.append(asset_values.sum())
        transaction_costs.append(daily_transaction_cost)

    portfolio_values = pd.Series(
        portfolio_values,
        index=returns.index,
        name="Portfolio Value"
    )

    transaction_costs = pd.Series(
        transaction_costs,
        index=returns.index,
        name="Transaction Costs"
    )

    return portfolio_values, transaction_costs


def calculate_rebalancing_metrics(
    portfolio_values,
    transaction_costs=None,
    trading_days=252,
    risk_free_rate=0.00
):
    """
    Calculates performance metrics for a rebalancing strategy.
    """
    daily_returns = portfolio_values.pct_change().dropna()

    final_value = portfolio_values.iloc[-1]
    total_return = final_value / portfolio_values.iloc[0] - 1

    annualized_return = (final_value / portfolio_values.iloc[0]) ** (
        trading_days / len(daily_returns)
    ) - 1

    annualized_volatility = daily_returns.std() * np.sqrt(trading_days)

    sharpe_ratio = (
        (annualized_return - risk_free_rate) / annualized_volatility
        if annualized_volatility != 0
        else np.nan
    )

    running_max = portfolio_values.cummax()
    drawdown = portfolio_values / running_max - 1
    max_drawdown = drawdown.min()

    total_transaction_costs = (
        transaction_costs.sum()
        if transaction_costs is not None
        else 0.00
    )

    return {
        "Final Value": final_value,
        "Total Return": total_return,
        "Annualized Return": annualized_return,
        "Annualized Volatility": annualized_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Maximum Drawdown": max_drawdown,
        "Total Transaction Costs": total_transaction_costs
    }


def compare_rebalancing_strategies(
    returns,
    portfolios,
    initial_value=10_000,
    trading_days=252,
    risk_free_rate=0.00
):
    """
    Compares Buy & Hold, Monthly, Quarterly, and Annual rebalancing strategies.
    """
    rebalancing_strategies = {
        "Buy & Hold": None,
        "Monthly Rebalancing": "M",
        "Quarterly Rebalancing": "Q",
        "Annual Rebalancing": "Y"
    }

    results = []
    portfolio_paths = {}

    for portfolio_name, weights in portfolios.items():
        portfolio_paths[portfolio_name] = {}

        for strategy_name, frequency in rebalancing_strategies.items():
            values = simulate_rebalanced_portfolio(
                returns=returns,
                weights=weights,
                initial_value=initial_value,
                rebalance_frequency=frequency
            )

            metrics = calculate_rebalancing_metrics(
                portfolio_values=values,
                trading_days=trading_days,
                risk_free_rate=risk_free_rate
            )

            metrics["Portfolio"] = portfolio_name
            metrics["Strategy"] = strategy_name

            results.append(metrics)
            portfolio_paths[portfolio_name][strategy_name] = values

    summary = pd.DataFrame(results)

    return summary, portfolio_paths


def compare_transaction_cost_rebalancing(
    returns,
    portfolios,
    initial_value=10_000,
    trading_days=252,
    risk_free_rate=0.00,
    transaction_cost_rates=None
):
    """
    Compares rebalancing strategies under multiple transaction cost assumptions.
    """
    if transaction_cost_rates is None:
        transaction_cost_rates = {
            "0.00%": 0.0000,
            "0.05%": 0.0005,
            "0.10%": 0.0010,
            "0.25%": 0.0025
        }

    rebalancing_strategies = {
        "Buy & Hold": None,
        "Monthly Rebalancing": "M",
        "Quarterly Rebalancing": "Q",
        "Annual Rebalancing": "Y"
    }

    results = []
    portfolio_paths = {}

    for portfolio_name, weights in portfolios.items():
        portfolio_paths[portfolio_name] = {}

        for strategy_name, frequency in rebalancing_strategies.items():
            portfolio_paths[portfolio_name][strategy_name] = {}

            for cost_label, cost_rate in transaction_cost_rates.items():
                values, costs = simulate_rebalanced_portfolio_with_costs(
                    returns=returns,
                    weights=weights,
                    initial_value=initial_value,
                    rebalance_frequency=frequency,
                    transaction_cost_rate=cost_rate
                )

                metrics = calculate_rebalancing_metrics(
                    portfolio_values=values,
                    transaction_costs=costs,
                    trading_days=trading_days,
                    risk_free_rate=risk_free_rate
                )

                metrics["Portfolio"] = portfolio_name
                metrics["Strategy"] = strategy_name
                metrics["Transaction Cost Rate"] = cost_label

                results.append(metrics)
                portfolio_paths[portfolio_name][strategy_name][cost_label] = values

    summary = pd.DataFrame(results)

    zero_cost_reference = summary[
        summary["Transaction Cost Rate"] == "0.00%"
    ][
        ["Portfolio", "Strategy", "Final Value"]
    ].rename(columns={"Final Value": "Zero Cost Final Value"})

    summary = summary.merge(
        zero_cost_reference,
        on=["Portfolio", "Strategy"],
        how="left"
    )

    summary["Cost Drag"] = (
        summary["Zero Cost Final Value"] - summary["Final Value"]
    )

    return summary, portfolio_paths


def get_best_strategy_by_metric(
    summary,
    metric="Sharpe Ratio",
    group_columns=None
):
    """
    Finds the best strategy by a selected metric.

    Default grouping:
    Portfolio + Transaction Cost Rate, if transaction cost data exists.
    """
    if group_columns is None:
        if "Transaction Cost Rate" in summary.columns:
            group_columns = ["Portfolio", "Transaction Cost Rate"]
        else:
            group_columns = ["Portfolio"]

    best_rows = summary.loc[
        summary.groupby(group_columns)[metric].idxmax()
    ]

    return best_rows.reset_index(drop=True)