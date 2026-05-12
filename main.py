"""
main.py - Entry point for Research Assistant Agent
Run this file to start the agent with a custom research topic
"""

from agent import create_agent
import os

def main():
    """Main entry point"""
    
    # ===== CONFIGURATION =====
    # Modify this topic to research something different
    RESEARCH_TOPIC = "Benefits of renewable energy"
    
    # Logging level: DEBUG, INFO, WARNING, ERROR
    LOG_LEVEL = 'INFO'
    
    # Use mock data (True = no API calls needed, False = real web search)
    USE_MOCK_DATA = False
    
    # ===== EXECUTE =====
    print("\n" + "="*70)
    print("RESEARCH ASSISTANT AGENT")
    print("="*70)
    print(f"Topic: {RESEARCH_TOPIC}")
    print(f"Mock Mode: {USE_MOCK_DATA}")
    print("="*70 + "\n")
    
    # Create agent
    agent = create_agent(log_level=LOG_LEVEL, use_mock=USE_MOCK_DATA)
    
    # Run research
    try:
        report = agent.run(RESEARCH_TOPIC)
        
        # Save report
        output_file = agent.save_report()
        
        # Print first part of report
        print("\n" + "="*70)
        print("REPORT PREVIEW")
        print("="*70)
        print(report[:1000])
        print("\n... (full report saved to file)")
        
        # Print summary
        print("\n" + "="*70)
        print("STATISTICS")
        print("="*70)
        summary = agent.get_state_summary()
        for key, value in summary.items():
            print(f"  {key:.<40} {value}")
        
        print(f"\n✓ Full report saved to: {output_file}")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    main()
