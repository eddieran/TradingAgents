import datetime
import os
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Custom config for deep research
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"
config["deep_think_llm"] = "o1-preview"  # Assuming 'o3' means o1-preview for deep reasoning
config["quick_think_llm"] = "gpt-4o-mini"
config["max_debate_rounds"] = 5  # Deep research: high debate rounds
config["max_risk_discuss_rounds"] = 5
config["online_tools"] = True

# Use all analysts by default
selected_analysts = ["market", "social", "news", "fundamentals"]

# Initialize the graph
ta = TradingAgentsGraph(selected_analysts, debug=False, config=config)

# Get today's date
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Run the analysis for TSLA
_, decision = ta.propagate("TSLA", today)

# Print the decision (optional, for logging)
print(decision)