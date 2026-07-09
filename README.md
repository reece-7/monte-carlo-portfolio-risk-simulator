# Interactive Portfolio Risk Analyzer

Interactive Portfolio Risk Analyzer is a Python-based portfolio analysis application that allows users to evaluate custom portfolios using historical market data, Monte Carlo simulations, risk metrics, portfolio optimization, rebalancing analysis, transaction costs, and benchmark sensitivity.

The project started as a quantitative finance notebook project and was later refactored into a reusable Python package with an interactive Streamlit interface.

---

## Live Demo

Try the app online:

https://rgraph.streamlit.app

---

## Features

The application allows users to input a custom portfolio and analyze it through several financial and risk-management tools.

### Portfolio Inputs

Users can customize:

- Initial capital
- Portfolio tickers
- Portfolio weights
- Historical start date
- Benchmark ticker
- Number of Monte Carlo simulations
- Monte Carlo time horizon
- Risk-free rate
- Trading days assumption
- Transaction cost assumptions

### Risk and Performance Analysis

The application calculates:

- Total return
- Annualized return
- Annualized volatility
- Sharpe Ratio
- Maximum drawdown
- Historical Value at Risk (VaR)
- Historical Expected Shortfall

### Monte Carlo Simulation

The project includes two Monte Carlo approaches:

- Parametric Monte Carlo simulation
- Historical Bootstrap Monte Carlo simulation

The simulations estimate:

- Mean final portfolio value
- Median final portfolio value
- Probability of loss
- Monte Carlo Value at Risk
- Monte Carlo Expected Shortfall

### Portfolio Optimization

The project includes:

- Efficient Frontier simulation
- Maximum Sharpe Ratio portfolio
- Minimum Volatility portfolio
- Risk Parity portfolio
- Asset risk contribution analysis

### Rebalancing and Transaction Costs

The application compares:

- Buy & Hold
- Monthly rebalancing
- Quarterly rebalancing
- Annual rebalancing

It also estimates the impact of transaction costs and calculates cost drag under different cost assumptions.

### Benchmark and Market Sensitivity

The project analyzes the portfolio relative to a selected benchmark using:

- Beta vs benchmark
- Correlation vs benchmark
- Tracking Error
- Information Ratio
- Upside Capture
- Downside Capture
- Rolling Beta

---

## Tech Stack

The project is built with:

- Python
- pandas
- NumPy
- SciPy
- matplotlib
- yfinance
- Streamlit
- Jupyter Notebook

---

## Project Structure

```text
Project_Montecarlo/
├── app.py
├── run_analysis.py
├── requirements.txt
├── README.md
├── data/
├── images/
├── notebooks/
├── outputs/
└── src/
    ├── __init__.py
    ├── data_loader.py
    ├── risk_metrics.py
    ├── monte_carlo.py
    ├── portfolio_optimization.py
    ├── rebalancing.py
    ├── market_sensitivity.py
    └── portfolio_analyzer.py
```

### Main Components

- `app.py`: interactive Streamlit application
- `run_analysis.py`: command-line version of the analysis
- `src/`: reusable Python modules
- `notebooks/`: research and development notebooks
- `outputs/`: generated CSV results
- `images/`: saved visualizations

---

## Installation

Clone the repository:

```bash
git clone https://github.com/reece-7/rgraph-portfolio-risk-analyzer.git
cd rgraph-portfolio-risk-analyzer
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## How to Run the Interactive App

Launch the Streamlit application:

```bash
streamlit run app.py
```

The application will open locally in the browser, usually at:

```text
http://localhost:8501
```

---

## How to Run the Command-Line Analysis

The project also includes a non-interactive script:

```bash
python run_analysis.py
```

This automatically runs a default portfolio analysis and saves the results in:

```text
outputs/final_analysis/
```

---

## Example Portfolio

The default portfolio used in the project is:

| Asset | Weight |
|---|---:|
| SPY | 40% |
| QQQ | 30% |
| TLT | 20% |
| GLD | 10% |

This represents a diversified portfolio with exposure to:

- U.S. equities
- Technology/growth equities
- Long-term Treasury bonds
- Gold

Users can replace these tickers and weights directly in the Streamlit interface.

---

## Example Outputs

The project generates several outputs, including:

- Portfolio performance summary
- Monte Carlo simulation results
- Efficient Frontier portfolios
- Optimal portfolio allocations
- Risk Parity weights
- Rebalancing strategy comparison
- Transaction cost analysis
- Market sensitivity metrics
- Rolling beta estimates

CSV outputs are saved in the `outputs/` folder.

---

## Methodology Overview

The project follows a quantitative portfolio analysis workflow:

```text
User inputs
↓
Historical price download
↓
Daily return calculation
↓
Portfolio performance analysis
↓
Risk metrics
↓
Monte Carlo simulation
↓
Portfolio optimization
↓
Rebalancing analysis
↓
Benchmark sensitivity
↓
Interactive results and downloadable outputs
```

The analysis is based on historical market data downloaded using `yfinance`.

---

## Important Notes

This project is designed for educational and analytical purposes.

The results should not be interpreted as financial advice. Monte Carlo simulations and historical risk metrics are based on past data and assumptions, and they do not guarantee future performance.

---

## Future Improvements

Possible future improvements include:

- More advanced visualizations
- Better ticker validation
- Asset type classification
- User-defined transaction costs
- Portfolio comparison mode
- Cloud deployment
- PDF report generation
- Improved UI design

---

## Author

Ouyang Sun
