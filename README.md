# Monte Carlo Portfolio Risk Simulator

This project uses Monte Carlo simulation to estimate the future value distribution and downside risk of a multi-asset investment portfolio.

## Assets
- SPY: S&P 500 ETF
- QQQ: Nasdaq 100 ETF
- TLT: Long-Term Treasury Bond ETF
- GLD: Gold ETF

## Methodology
The project uses historical daily returns, volatility, and asset correlations to simulate 10,000 possible one-year portfolio outcomes.

## Risk Metrics
- Probability of Loss
- 95% Value at Risk
- 95% Expected Shortfall
- Final Portfolio Value Distribution

## Tools
Python, pandas, numpy, matplotlib, yfinance, scipy, Jupyter Notebook