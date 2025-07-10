#!/usr/bin/env python3
"""
Simple test script to verify that the tradingagents module can be imported.
This is useful for debugging import issues in CI/CD environments.
"""

import sys
import os

def test_imports():
    """Test importing the main modules."""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        print("✅ TradingAgentsGraph imported successfully")
        
        from tradingagents.default_config import DEFAULT_CONFIG
        print("✅ DEFAULT_CONFIG imported successfully")
        
        from cli.models import AnalystType
        print("✅ AnalystType imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(f"Python path: {sys.path}")
        print(f"Current directory: {os.getcwd()}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 