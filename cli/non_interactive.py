#!/usr/bin/env python3
"""
Non-interactive version of TradingAgents CLI for use in CI/CD environments like GitHub Actions.
This script uses environment variables for configuration instead of interactive prompts.
"""

import os
import sys
import datetime
from pathlib import Path
from typing import Optional

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from cli.models import AnalystType


def get_env_or_default(key: str, default: str) -> str:
    """Get value from environment variable or return default."""
    return os.getenv(key, default)


def get_env_or_fail(key: str) -> str:
    """Get value from environment variable or fail if not set."""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable {key} is required but not set")
    return value


def run_non_interactive_analysis():
    """Run TradingAgents analysis with environment variable configuration."""
    
    # Get required parameters from environment variables
    ticker = get_env_or_fail("TRADINGAGENTS_TICKER")
    analysis_date = get_env_or_default("TRADINGAGENTS_DATE", datetime.date.today().strftime("%Y-%m-%d"))
    
    # Get optional configuration from environment variables
    deep_think_llm = get_env_or_default("TRADINGAGENTS_DEEP_THINK_LLM", "o4-mini")
    quick_think_llm = get_env_or_default("TRADINGAGENTS_QUICK_THINK_LLM", "gpt-4o-mini")
    max_debate_rounds = int(get_env_or_default("TRADINGAGENTS_MAX_DEBATE_ROUNDS", "1"))
    online_tools = get_env_or_default("TRADINGAGENTS_ONLINE_TOOLS", "true").lower() == "true"
    debug = get_env_or_default("TRADINGAGENTS_DEBUG", "false").lower() == "true"
    
    # Create custom configuration
    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = deep_think_llm
    config["quick_think_llm"] = quick_think_llm
    config["max_debate_rounds"] = max_debate_rounds
    config["online_tools"] = online_tools
    
    print(f"🚀 Starting TradingAgents analysis for {ticker} on {analysis_date}")
    print(f"📊 Configuration:")
    print(f"   - Deep Think LLM: {deep_think_llm}")
    print(f"   - Quick Think LLM: {quick_think_llm}")
    print(f"   - Max Debate Rounds: {max_debate_rounds}")
    print(f"   - Online Tools: {online_tools}")
    print(f"   - Debug Mode: {debug}")
    print()
    
    try:
        # Initialize TradingAgents with custom config
        ta = TradingAgentsGraph(debug=debug, config=config)
        
        # Run the analysis
        print("🔄 Running analysis...")
        _, decision = ta.propagate(ticker, analysis_date)
        
        print("✅ Analysis completed successfully!")
        print("\n📋 Final Decision:")
        print("=" * 50)
        print(decision)
        print("=" * 50)
        
        # Save results to file if output path is specified
        output_path = os.getenv("TRADINGAGENTS_OUTPUT_PATH")
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(f"# TradingAgents Analysis Report\n")
                f.write(f"**Ticker:** {ticker}\n")
                f.write(f"**Date:** {analysis_date}\n")
                f.write(f"**Generated:** {datetime.datetime.now().isoformat()}\n\n")
                f.write(f"## Final Decision\n\n{decision}\n")
            print(f"💾 Results saved to: {output_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return 1


if __name__ == "__main__":
    # Check if required API keys are set
    required_keys = ["OPENAI_API_KEY", "FINNHUB_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"❌ Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set these environment variables before running the analysis.")
        sys.exit(1)
    
    # Run the analysis
    exit_code = run_non_interactive_analysis()
    sys.exit(exit_code) 