import pandas as pd
import streamlit as st

from src.portfolio_analyzer import analyze_portfolio


st.set_page_config(
    page_title="Interactive Portfolio Risk Analyzer",
    layout="wide"
)


st.title("Interactive Portfolio Risk Analyzer")

st.write(
    """
    Analyze a custom portfolio using historical returns, Monte Carlo simulations,
    rebalancing analysis, transaction costs, risk parity, and benchmark sensitivity.
    """
)


# =========================
# SIDEBAR INPUTS
# =========================

st.sidebar.header("Portfolio Inputs")

initial_value = st.sidebar.number_input(
    "Initial capital",
    min_value=100.0,
    value=10_000.0,
    step=1_000.0
)

start_date = st.sidebar.date_input(
    "Start date",
    value=pd.to_datetime("2018-01-01")
)

benchmark_ticker = st.sidebar.text_input(
    "Benchmark ticker",
    value="SPY"
).upper().strip()

n_simulations = st.sidebar.number_input(
    "Number of Monte Carlo simulations",
    min_value=500,
    max_value=50_000,
    value=2_000,
    step=500
)

time_horizon = st.sidebar.number_input(
    "Monte Carlo horizon in trading days",
    min_value=21,
    max_value=2520,
    value=252,
    step=21
)

risk_free_rate_percent = st.sidebar.number_input(
    "Risk-free rate (%)",
    min_value=0.0,
    max_value=20.0,
    value=0.0,
    step=0.25
)

risk_free_rate = risk_free_rate_percent / 100

trading_days = st.sidebar.selectbox(
    "Trading days assumption",
    options=[252, 365],
    index=0,
    help="Use 252 for stocks/ETFs and 365 for crypto-heavy portfolios."
)


st.sidebar.header("Assets")

number_of_assets = st.sidebar.number_input(
    "How many assets are in your portfolio?",
    min_value=2,
    max_value=10,
    value=4,
    step=1
)


default_tickers = ["SPY", "QQQ", "TLT", "GLD"]
default_weights = [40.0, 30.0, 20.0, 10.0]

tickers = []
weights_percent = []

for i in range(number_of_assets):
    default_ticker = default_tickers[i] if i < len(default_tickers) else ""
    default_weight = default_weights[i] if i < len(default_weights) else 0.0

    col1, col2 = st.sidebar.columns(2)

    ticker = col1.text_input(
        f"Asset {i + 1} ticker",
        value=default_ticker,
        key=f"ticker_{i}"
    ).upper().strip()

    weight = col2.number_input(
        f"Weight {i + 1} (%)",
        min_value=0.0,
        max_value=100.0,
        value=default_weight,
        step=1.0,
        key=f"weight_{i}"
    )

    tickers.append(ticker)
    weights_percent.append(weight)


weights = {
    ticker: weight / 100
    for ticker, weight in zip(tickers, weights_percent)
    if ticker != ""
}

weight_sum = sum(weights.values())


# =========================
# INPUT CHECKS
# =========================

st.subheader("Portfolio Setup")

setup_df = pd.DataFrame({
    "Ticker": list(weights.keys()),
    "Weight": list(weights.values())
})

if not setup_df.empty:
    setup_df["Weight (%)"] = setup_df["Weight"] * 100
    st.dataframe(setup_df[["Ticker", "Weight (%)"]], use_container_width=True)

st.write(f"Total weight: **{weight_sum * 100:.2f}%**")

if abs(weight_sum - 1.0) > 0.0001:
    st.warning("Portfolio weights must sum to 100% before running the analysis.")

if len(weights) < 2:
    st.warning("Please enter at least two valid tickers.")


# =========================
# RUN ANALYSIS
# =========================

run_button = st.button("Run Portfolio Analysis")

if run_button:
    if abs(weight_sum - 1.0) > 0.0001:
        st.error("Cannot run analysis: weights must sum to 100%.")
    elif len(weights) < 2:
        st.error("Cannot run analysis: please enter at least two valid tickers.")
    else:
        with st.spinner("Running portfolio analysis..."):
            try:
                results = analyze_portfolio(
                    tickers=list(weights.keys()),
                    weights=weights,
                    start_date=str(start_date),
                    end_date=None,
                    initial_value=initial_value,
                    n_simulations=int(n_simulations),
                    time_horizon=int(time_horizon),
                    trading_days=int(trading_days),
                    risk_free_rate=risk_free_rate,
                    benchmark_ticker=benchmark_ticker,
                    transaction_cost_rates={
                        "0.00%": 0.0000,
                        "0.05%": 0.0005,
                        "0.10%": 0.0010,
                        "0.25%": 0.0025
                    }
                )

                st.success("Analysis completed successfully.")

                # =========================
                # PERFORMANCE SUMMARY
                # =========================

                st.header("Performance Summary")

                performance_summary = pd.DataFrame(
                    [results["performance_summary"]],
                    index=["Custom Portfolio"]
                )

                st.dataframe(performance_summary, use_container_width=True)

                st.subheader("Portfolio Value Over Time")
                st.line_chart(results["portfolio_values"])

                # =========================
                # MONTE CARLO
                # =========================

                st.header("Monte Carlo Simulation")

                st.dataframe(
                    results["monte_carlo_comparison"],
                    use_container_width=True
                )

                st.subheader("Monte Carlo Final Value Distribution")

                monte_carlo_final_values = pd.DataFrame({
                    "Parametric Monte Carlo": results["parametric_final_values"],
                    "Bootstrap Monte Carlo": results["bootstrap_final_values"]
                })

                st.dataframe(
                    monte_carlo_final_values.describe(),
                    use_container_width=True
                )

                # =========================
                # OPTIMIZATION
                # =========================

                st.header("Portfolio Optimization")

                st.subheader("Optimal Portfolios")
                st.dataframe(
                    results["optimal_portfolios"],
                    use_container_width=True
                )

                st.subheader("Risk Parity Weights")

                risk_parity_df = results["risk_parity_weights"].to_frame(
                    name="Weight"
                )

                risk_parity_df["Weight (%)"] = risk_parity_df["Weight"] * 100

                st.dataframe(risk_parity_df, use_container_width=True)

                # =========================
                # REBALANCING
                # =========================

                st.header("Rebalancing Analysis")

                st.dataframe(
                    results["rebalancing_summary"],
                    use_container_width=True
                )

                st.header("Transaction Cost Analysis")

                st.dataframe(
                    results["transaction_cost_summary"],
                    use_container_width=True
                )

                # =========================
                # MARKET SENSITIVITY
                # =========================

                st.header("Market Sensitivity")

                st.subheader("Benchmark Sensitivity")
                st.dataframe(
                    results["market_sensitivity_summary"],
                    use_container_width=True
                )

                st.subheader("Upside / Downside Capture")
                st.dataframe(
                    results["capture_summary"],
                    use_container_width=True
                )

                st.subheader("Rolling Beta")
                st.line_chart(results["rolling_beta"])

                # =========================
                # DOWNLOADS
                # =========================

                st.header("Download Results")

                csv = performance_summary.to_csv().encode("utf-8")

                st.download_button(
                    label="Download Performance Summary CSV",
                    data=csv,
                    file_name="performance_summary.csv",
                    mime="text/csv"
                )

            except Exception as error:
                st.error("An error occurred while running the analysis.")
                st.exception(error)