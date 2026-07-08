import numpy as np
import pandas as pd
from scipy.optimize import minimize


def calculate_portfolio_return(weights, mean_returns, trading_days=252):
    """
    Calculates annualized portfolio return.
    """
    return np.dot(weights, mean_returns) * trading_days


def calculate_portfolio_volatility(weights, cov_matrix, trading_days=252):
    """
    Calculates annualized portfolio volatility.
    """
    annualized_cov_matrix = cov_matrix * trading_days
    return np.sqrt(weights.T @ annualized_cov_matrix @ weights)


def calculate_portfolio_sharpe_ratio(
    weights,
    mean_returns,
    cov_matrix,
    trading_days=252,
    risk_free_rate=0.00
):
    """
    Calculates portfolio Sharpe Ratio.
    """
    portfolio_return = calculate_portfolio_return(
        weights,
        mean_returns,
        trading_days=trading_days
    )

    portfolio_volatility = calculate_portfolio_volatility(
        weights,
        cov_matrix,
        trading_days=trading_days
    )

    if portfolio_volatility == 0:
        return np.nan

    return (portfolio_return - risk_free_rate) / portfolio_volatility


def generate_random_portfolios(
    returns,
    n_portfolios=20_000,
    trading_days=252,
    risk_free_rate=0.00,
    random_seed=42
):
    """
    Generates random portfolio allocations and calculates return, volatility,
    Sharpe Ratio, and asset weights.
    """
    np.random.seed(random_seed)

    assets = returns.columns
    n_assets = len(assets)

    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    portfolio_results = []

    for _ in range(n_portfolios):
        weights = np.random.random(n_assets)
        weights = weights / weights.sum()

        annualized_return = calculate_portfolio_return(
            weights,
            mean_returns,
            trading_days=trading_days
        )

        annualized_volatility = calculate_portfolio_volatility(
            weights,
            cov_matrix,
            trading_days=trading_days
        )

        sharpe_ratio = (
            (annualized_return - risk_free_rate) / annualized_volatility
            if annualized_volatility != 0
            else np.nan
        )

        result = {
            "Annualized Return": annualized_return,
            "Annualized Volatility": annualized_volatility,
            "Sharpe Ratio": sharpe_ratio
        }

        for asset, weight in zip(assets, weights):
            result[f"Weight {asset}"] = weight

        portfolio_results.append(result)

    return pd.DataFrame(portfolio_results)


def identify_optimal_portfolios(efficient_frontier_df):
    """
    Identifies Maximum Sharpe and Minimum Volatility portfolios.
    """
    max_sharpe_portfolio = efficient_frontier_df.loc[
        efficient_frontier_df["Sharpe Ratio"].idxmax()
    ]

    min_volatility_portfolio = efficient_frontier_df.loc[
        efficient_frontier_df["Annualized Volatility"].idxmin()
    ]

    optimal_portfolios = pd.DataFrame({
        "Maximum Sharpe Portfolio": max_sharpe_portfolio,
        "Minimum Volatility Portfolio": min_volatility_portfolio
    }).T

    return optimal_portfolios


def portfolio_volatility(weights, cov_matrix):
    """
    Calculates portfolio volatility using a covariance matrix.
    """
    return np.sqrt(weights.T @ cov_matrix @ weights)


def risk_contributions(weights, cov_matrix):
    """
    Calculates each asset's percentage contribution to total portfolio risk.
    """
    portfolio_vol = portfolio_volatility(weights, cov_matrix)

    marginal_contribution = cov_matrix @ weights
    absolute_risk_contribution = weights * marginal_contribution / portfolio_vol
    percentage_risk_contribution = absolute_risk_contribution / portfolio_vol

    return percentage_risk_contribution


def risk_parity_objective(weights, cov_matrix):
    """
    Objective function for Risk Parity optimization.
    """
    target_risk_contribution = np.ones(len(weights)) / len(weights)
    actual_risk_contribution = risk_contributions(weights, cov_matrix)

    return np.sum((actual_risk_contribution - target_risk_contribution) ** 2)


def calculate_risk_parity_weights(returns, trading_days=252):
    """
    Calculates long-only Risk Parity portfolio weights.
    """
    assets = returns.columns
    n_assets = len(assets)

    cov_matrix = returns.cov() * trading_days

    initial_guess = np.ones(n_assets) / n_assets

    constraints = (
        {
            "type": "eq",
            "fun": lambda weights: np.sum(weights) - 1
        },
    )

    bounds = tuple((0, 1) for _ in range(n_assets))

    solution = minimize(
        fun=risk_parity_objective,
        x0=initial_guess,
        args=(cov_matrix,),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    risk_parity_weights = pd.Series(
        solution.x,
        index=assets,
        name="Risk Parity"
    )

    return risk_parity_weights


def compare_portfolio_weights(returns, custom_weights=None):
    """
    Compares Equal Weight, optional custom weights, and Risk Parity weights.
    """
    assets = returns.columns
    n_assets = len(assets)

    equal_weight = pd.Series(
        np.ones(n_assets) / n_assets,
        index=assets,
        name="Equal Weight"
    )

    risk_parity_weight = calculate_risk_parity_weights(returns)

    weights_dict = {
        "Equal Weight": equal_weight,
        "Risk Parity": risk_parity_weight
    }

    if custom_weights is not None:
        custom_weights = pd.Series(custom_weights)
        custom_weights = custom_weights[assets]
        custom_weights.name = "Custom Portfolio"
        weights_dict["Custom Portfolio"] = custom_weights

    weights_comparison = pd.DataFrame(weights_dict)

    return weights_comparison


def calculate_risk_contribution_comparison(returns, weights_comparison, trading_days=252):
    """
    Calculates risk contribution comparison across multiple portfolios.
    """
    cov_matrix = returns.cov() * trading_days

    risk_contribution_comparison = pd.DataFrame()

    for portfolio_name in weights_comparison.columns:
        weights = weights_comparison[portfolio_name].values

        risk_contribution_comparison[portfolio_name] = risk_contributions(
            weights,
            cov_matrix
        )

    risk_contribution_comparison.index = returns.columns

    return risk_contribution_comparison