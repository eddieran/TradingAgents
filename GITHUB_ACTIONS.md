# GitHub Actions for TradingAgents

This document explains how to set up and use GitHub Actions to run TradingAgents analysis automatically.

## Overview

We've created two GitHub Actions workflows:

1. **Manual TradingAgents Analysis** (`.github/workflows/manual-analysis.yml`) - Simple workflow for manual triggering
2. **TradingAgents Analysis** (`.github/workflows/trading-analysis.yml`) - Advanced workflow with more configuration options

## Setup

### 1. Add Repository Secrets

You need to add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `FINNHUB_API_KEY`: Your FinnHub API key

### 2. Enable GitHub Actions

The workflows will be automatically available once you push them to your repository. You can find them in the **Actions** tab.

## Usage

### Manual Analysis (Recommended for beginners)

1. Go to the **Actions** tab in your repository
2. Select **Manual TradingAgents Analysis**
3. Click **Run workflow**
4. Fill in the required fields:
   - **Ticker**: Stock symbol (e.g., `NVDA`, `AAPL`, `TSLA`)
   - **Date**: Analysis date in YYYY-MM-DD format (leave empty for today)
5. Click **Run workflow**

### Advanced Analysis

1. Go to the **Actions** tab in your repository
2. Select **TradingAgents Analysis**
3. Click **Run workflow**
4. Configure all the parameters as needed:
   - **Ticker**: Stock symbol
   - **Date**: Analysis date
   - **Deep Think LLM**: Model for deep thinking (default: `o4-mini`)
   - **Quick Think LLM**: Model for quick thinking (default: `gpt-4o-mini`)
   - **Max Debate Rounds**: Number of debate rounds (default: `1`)
   - **Online Tools**: Whether to use online tools (default: `true`)
   - **Debug**: Enable debug mode (default: `false`)

## Environment Variables

The non-interactive script (`cli/non_interactive.py`) uses the following environment variables:

### Required
- `TRADINGAGENTS_TICKER`: Stock ticker symbol to analyze
- `OPENAI_API_KEY`: Your OpenAI API key
- `FINNHUB_API_KEY`: Your FinnHub API key

### Optional
- `TRADINGAGENTS_DATE`: Analysis date (default: today)
- `TRADINGAGENTS_DEEP_THINK_LLM`: Deep thinking LLM model (default: `o4-mini`)
- `TRADINGAGENTS_QUICK_THINK_LLM`: Quick thinking LLM model (default: `gpt-4o-mini`)
- `TRADINGAGENTS_MAX_DEBATE_ROUNDS`: Maximum debate rounds (default: `1`)
- `TRADINGAGENTS_ONLINE_TOOLS`: Use online tools (default: `true`)
- `TRADINGAGENTS_DEBUG`: Enable debug mode (default: `false`)
- `TRADINGAGENTS_OUTPUT_PATH`: Path to save results (optional)

## Results

After the workflow completes:

1. **Artifacts**: Analysis results are saved as GitHub artifacts that you can download
2. **Logs**: Full execution logs are available in the workflow run
3. **Output**: The final decision and analysis are displayed in the workflow output

## Scheduled Runs

The advanced workflow includes a scheduled run that executes daily at 9 AM UTC on weekdays (Monday-Friday). You can modify the schedule in the workflow file:

```yaml
schedule:
  - cron: '0 9 * * 1-5'  # Daily at 9 AM UTC, Monday-Friday
```

## Local Testing

You can test the non-interactive script locally:

```bash
# Set environment variables
export OPENAI_API_KEY="your-openai-api-key"
export FINNHUB_API_KEY="your-finnhub-api-key"
export TRADINGAGENTS_TICKER="NVDA"
export TRADINGAGENTS_DATE="2024-01-15"

# Install the package in development mode
pip install -e .

# Run the analysis
python cli/non_interactive.py
```

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure both `OPENAI_API_KEY` and `FINNHUB_API_KEY` are set as repository secrets
2. **Invalid Ticker**: Make sure the ticker symbol is valid and exists
3. **Date Format**: Use YYYY-MM-DD format for dates
4. **API Limits**: Be aware of OpenAI and FinnHub API rate limits

### Debug Mode

Enable debug mode to get more detailed output:

```yaml
TRADINGAGENTS_DEBUG: true
```

### Cost Optimization

To reduce API costs:
- Use `o4-mini` and `gpt-4o-mini` models
- Set `max_debate_rounds` to `1`
- Use `online_tools: false` if you have cached data

## Customization

You can customize the workflows by:

1. Modifying the workflow files in `.github/workflows/`
2. Adding new environment variables to the non-interactive script
3. Creating new workflows for specific use cases

## Security Notes

- Never commit API keys to your repository
- Use GitHub Secrets for sensitive information
- Consider using different API keys for testing vs production
- Monitor your API usage to avoid unexpected costs 