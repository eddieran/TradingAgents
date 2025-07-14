import datetime
import os
import sys
from pathlib import Path
from functools import wraps

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from cli.models import AnalystType

def run_automated_analysis(dry_run=False):
    """Run automated analysis for TSLA with predefined settings."""
    
    # Hardcoded selections for automation
    selections = {
        "ticker": "TSLA",
        "analysis_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "analysts": [AnalystType.MARKET, AnalystType.SOCIAL, AnalystType.NEWS, AnalystType.FUNDAMENTALS],
        "research_depth": 5,  # Deep research
        "llm_provider": "openai",
        "backend_url": "https://api.openai.com/v1",
        "shallow_thinker": "gpt-4o-mini",
        "deep_thinker": "o3",  # Deep reasoning model
    }
    
    print(f"Starting automated TSLA analysis for {selections['analysis_date']}")
    print(f"Using analysts: {', '.join(analyst.value for analyst in selections['analysts'])}")
    print(f"Research depth: {selections['research_depth']} (Deep)")
    print(f"Deep thinking model: {selections['deep_thinker']}")
    
    if dry_run:
        print("DRY RUN: Skipping actual analysis")
        return "DRY_RUN_HOLD"
    
    # Create config with selected research depth
    config = DEFAULT_CONFIG.copy()
    config["max_debate_rounds"] = selections["research_depth"]
    config["max_risk_discuss_rounds"] = selections["research_depth"]
    config["quick_think_llm"] = selections["shallow_thinker"]
    config["deep_think_llm"] = selections["deep_thinker"]
    config["backend_url"] = selections["backend_url"]
    config["llm_provider"] = selections["llm_provider"].lower()
    config["online_tools"] = True

    # Check for required environment variables
    required_env_vars = ["OPENAI_API_KEY", "FINNHUB_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
        return None

    try:
        # Initialize the graph
        graph = TradingAgentsGraph(
            [analyst.value for analyst in selections["analysts"]], 
            config=config, 
            debug=False  # Set to False for automation
        )

        # Create result directory
        results_dir = Path(config["results_dir"]) / selections["ticker"] / selections["analysis_date"]
        results_dir.mkdir(parents=True, exist_ok=True)
        report_dir = results_dir / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        log_file = results_dir / "message_tool.log"
        log_file.touch(exist_ok=True)

        print(f"Results will be saved to: {results_dir}")
        print("Running analysis...")
        
        # Run the analysis using the propagate method
        final_state, decision = graph.propagate(selections["ticker"], selections["analysis_date"])
        
        # Save reports to files
        report_sections = {
            "market_report": final_state.get("market_report"),
            "sentiment_report": final_state.get("sentiment_report"), 
            "news_report": final_state.get("news_report"),
            "fundamentals_report": final_state.get("fundamentals_report"),
            "investment_plan": final_state.get("investment_plan"),
            "trader_investment_plan": final_state.get("trader_investment_plan"),
            "final_trade_decision": final_state.get("final_trade_decision"),
        }
        
        # Save each report section to a file
        for section_name, content in report_sections.items():
            if content:
                file_name = f"{section_name}.md"
                with open(report_dir / file_name, "w") as f:
                    f.write(content)
                print(f"Saved {section_name} to {file_name}")
        
        # Write summary to log
        with open(log_file, "w") as f:
            f.write(f"Analysis completed at {datetime.datetime.now()}\n")
            f.write(f"Ticker: {selections['ticker']}\n")
            f.write(f"Date: {selections['analysis_date']}\n")
            f.write(f"Decision: {decision}\n")
        
        print(f"Analysis complete! Decision: {decision}")
        print(f"Reports saved to: {report_dir}")
        
        return decision
        
    except Exception as e:
        print(f"ERROR: Analysis failed with exception: {str(e)}")
        return None

if __name__ == "__main__":
    # Check if dry run is requested
    dry_run = len(sys.argv) > 1 and sys.argv[1] == "--dry-run"
    result = run_automated_analysis(dry_run=dry_run)
    
    if result is None:
        sys.exit(1)
    else:
        print(f"Final result: {result}")
        sys.exit(0)