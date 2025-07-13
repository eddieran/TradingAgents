# Daily Analysis Automation

This directory contains scripts for automating the TradingAgents analysis process.

## Scripts

### `daily_analysis.py`

Automated daily analysis script for TSLA stock using deep research configuration.

**Features:**
- Runs analysis for TSLA with all 4 analysts (market, social, news, fundamentals)
- Uses deep research mode (5 debate/discussion rounds)
- Configured for o1-preview (deep thinking) and gpt-4o-mini (quick thinking)
- Saves all reports to `results/TSLA/YYYY-MM-DD/reports/`
- Includes error handling and environment variable validation

**Usage:**

```bash
# Run the analysis
PYTHONPATH=/path/to/TradingAgents python scripts/daily_analysis.py

# Dry run (for testing)
PYTHONPATH=/path/to/TradingAgents python scripts/daily_analysis.py --dry-run
```

**Required Environment Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `FINNHUB_API_KEY`: Your Finnhub API key for financial data

## GitHub Actions Automation

The analysis runs automatically daily at midnight UTC via GitHub Actions (`.github/workflows/daily-tsla-analysis.yml`).

**Setup Requirements:**
1. Add the following secrets to your GitHub repository:
   - `OPENAI_API_KEY`
   - `FINNHUB_API_KEY`

2. The workflow will:
   - Install dependencies
   - Run the analysis
   - Commit results back to the repository

**Manual Triggering:**
You can also trigger the workflow manually from the GitHub Actions tab.

## Configuration

The script uses the following default configuration:

- **Ticker**: TSLA
- **Research Depth**: 5 (Deep)
- **Deep Thinking Model**: o1-preview
- **Quick Thinking Model**: gpt-4o-mini
- **Analysts**: Market, Social, News, Fundamentals
- **Online Tools**: Enabled

To modify these settings, edit the `selections` dictionary in `daily_analysis.py`.

## Output

The script generates the following files in `results/TSLA/YYYY-MM-DD/`:

- `reports/market_report.md` - Market analysis
- `reports/sentiment_report.md` - Social media sentiment analysis  
- `reports/news_report.md` - News analysis
- `reports/fundamentals_report.md` - Fundamental analysis
- `reports/investment_plan.md` - Research team investment plan
- `reports/trader_investment_plan.md` - Trader's plan
- `reports/final_trade_decision.md` - Final trading decision
- `message_tool.log` - Analysis log summary 