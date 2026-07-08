from pathlib import Path
import pandas as pd

from src.portfolio_analyzer import analyze_portfolio


# =========================
# USER INPUTS
# =========================

TICKERS = ["SPY", "QQQ", "TLT", "GLD"]

WEIGHTS = {
    "SPY": 0.40,
    "QQQ": 0.30,
    "TLT": 0.20,
    "GLD": 0.10
}

START_DATE = "2018-01-01"
END_DATE = None

INITIAL_VALUE = 10_000
N_SIMULATIONS = 5_000
TIME_HORIZON = 252

TRADING_DAYS = 252
RISK_FREE_RATE = 0.00
BENCHMARK_TICKER = "SPY"

TRANSACTION_COST_RATES = {
    "0.00%": 0.0000,
    "0.05%": 0.0005,
    "0.10%": 0.0010,
    "0.25%": 0.0025
}


# =========================
# OUTPUT SETTINGS
# =========================

OUTPUT_DIR = Path("outputs/final_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_results(results, output_dir):
    """
    Saves the main analysis results as CSV files.
    """

    pd.DataFrame(
        [results["performance_summary"]],
        index=["Custom Portfolio"]
    ).to_csv(output_dir / "performance_summary.csv")

    results["monte_carlo_comparison"].to_csv(
        output_dir / "monte_carlo_comparison.csv"
    )

    results["risk_parity_weights"].to_frame(
        name="Weight"
    ).to_csv(output_dir / "risk_parity_weights.csv")

    results["optimal_portfolios"].to_csv(
        output_dir / "optimal_portfolios.csv"
    )

    results["rebalancing_summary"].to_csv(
        output_dir / "rebalancing_summary.csv",
        index=False
    )

    results["transaction_cost_summary"].to_csv(
        output_dir / "transaction_cost_summary.csv",
        index=False
    )

    results["market_sensitivity_summary"].to_csv(
        output_dir / "market_sensitivity_summary.csv"
    )

    results["capture_summary"].to_csv(
        output_dir / "capture_summary.csv"
    )

    results["portfolio_values"].to_frame(
        name="Portfolio Value"
    ).to_csv(output_dir / "portfolio_values.csv")

    results["rolling_beta"].to_csv(
        output_dir / "rolling_beta.csv"
    )

    results["efficient_frontier"].to_csv(
        output_dir / "efficient_frontier.csv",
        index=False
    )

    pd.DataFrame({
        "Parametric Final Value": results["parametric_final_values"],
        "Bootstrap Final Value": results["bootstrap_final_values"]
    }).to_csv(
        output_dir / "monte_carlo_final_values.csv",
        index=False
    )


def main():
    print("Running portfolio analysis...")

    results = analyze_portfolio(
        tickers=TICKERS,
        weights=WEIGHTS,
        start_date=START_DATE,
        end_date=END_DATE,
        initial_value=INITIAL_VALUE,
        n_simulations=N_SIMULATIONS,
        time_horizon=TIME_HORIZON,
        trading_days=TRADING_DAYS,
        risk_free_rate=RISK_FREE_RATE,
        benchmark_ticker=BENCHMARK_TICKER,
        transaction_cost_rates=TRANSACTION_COST_RATES
    )

    save_results(results, OUTPUT_DIR)

    print("\nAnalysis completed successfully.")
    print(f"Results saved in: {OUTPUT_DIR}")

    print("\nPerformance Summary:")
    print(pd.DataFrame([results["performance_summary"]], index=["Custom Portfolio"]))

    print("\nMonte Carlo Comparison:")
    print(results["monte_carlo_comparison"])

    print("\nRisk Parity Weights:")
    print(results["risk_parity_weights"])

    print("\nMarket Sensitivity:")
    print(results["market_sensitivity_summary"])


if __name__ == "__main__":
    main()