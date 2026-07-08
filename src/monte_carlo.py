import numpy as np
import pandas as pd


def run_parametric_monte_carlo(
    returns,
    weights,
    initial_value=10_000,
    n_simulations=10_000,
    time_horizon=252,
    random_seed=42
):
    """
    Runs a parametric Monte Carlo simulation using historical mean returns
    and covariance matrix.

    Returns:
    - portfolio_values: simulated portfolio value paths
    - final_values: final portfolio values at the end of the horizon
    """
    np.random.seed(random_seed)

    weights = pd.Series(weights)
    weights = weights[returns.columns]

    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    simulated_asset_returns = np.random.multivariate_normal(
        mean=mean_returns,
        cov=cov_matrix,
        size=(n_simulations, time_horizon)
    )

    simulated_portfolio_returns = simulated_asset_returns @ weights.values

    portfolio_values = initial_value * np.cumprod(
        1 + simulated_portfolio_returns,
        axis=1
    )

    final_values = portfolio_values[:, -1]

    return portfolio_values, final_values


def run_bootstrap_monte_carlo(
    returns,
    weights,
    initial_value=10_000,
    n_simulations=10_000,
    time_horizon=252,
    random_seed=42
):
    """
    Runs a historical bootstrap Monte Carlo simulation.

    Each simulated path is created by randomly sampling historical daily returns
    with replacement.
    """
    np.random.seed(random_seed)

    weights = pd.Series(weights)
    weights = weights[returns.columns]

    historical_returns = returns.values
    n_observations = historical_returns.shape[0]

    random_indices = np.random.randint(
        low=0,
        high=n_observations,
        size=(n_simulations, time_horizon)
    )

    sampled_asset_returns = historical_returns[random_indices]

    simulated_portfolio_returns = sampled_asset_returns @ weights.values

    portfolio_values = initial_value * np.cumprod(
        1 + simulated_portfolio_returns,
        axis=1
    )

    final_values = portfolio_values[:, -1]

    return portfolio_values, final_values


def calculate_simulation_risk_metrics(
    final_values,
    initial_value=10_000,
    confidence_level=0.95
):
    """
    Calculates risk metrics from simulated final portfolio values.
    """
    simulated_returns = final_values / initial_value - 1

    percentile = (1 - confidence_level) * 100

    value_at_risk = np.percentile(simulated_returns, percentile)

    expected_shortfall = simulated_returns[
        simulated_returns <= value_at_risk
    ].mean()

    probability_of_loss = np.mean(final_values < initial_value)

    metrics = {
        "Mean Final Value": final_values.mean(),
        "Median Final Value": np.median(final_values),
        "Probability of Loss": probability_of_loss,
        f"{int(confidence_level * 100)}% Value at Risk": value_at_risk,
        f"{int(confidence_level * 100)}% Expected Shortfall": expected_shortfall
    }

    return metrics


def compare_monte_carlo_methods(
    returns,
    weights,
    initial_value=10_000,
    n_simulations=10_000,
    time_horizon=252,
    confidence_level=0.95,
    random_seed=42
):
    """
    Compares Parametric Monte Carlo and Bootstrap Monte Carlo methods.
    """
    parametric_paths, parametric_final_values = run_parametric_monte_carlo(
        returns=returns,
        weights=weights,
        initial_value=initial_value,
        n_simulations=n_simulations,
        time_horizon=time_horizon,
        random_seed=random_seed
    )

    bootstrap_paths, bootstrap_final_values = run_bootstrap_monte_carlo(
        returns=returns,
        weights=weights,
        initial_value=initial_value,
        n_simulations=n_simulations,
        time_horizon=time_horizon,
        random_seed=random_seed
    )

    parametric_metrics = calculate_simulation_risk_metrics(
        parametric_final_values,
        initial_value=initial_value,
        confidence_level=confidence_level
    )

    bootstrap_metrics = calculate_simulation_risk_metrics(
        bootstrap_final_values,
        initial_value=initial_value,
        confidence_level=confidence_level
    )

    comparison = pd.DataFrame({
        "Parametric Monte Carlo": parametric_metrics,
        "Bootstrap Monte Carlo": bootstrap_metrics
    }).T

    results = {
        "comparison": comparison,
        "parametric_paths": parametric_paths,
        "parametric_final_values": parametric_final_values,
        "bootstrap_paths": bootstrap_paths,
        "bootstrap_final_values": bootstrap_final_values
    }

    return results