"""
demo.py - Demonstration of Research Assistant Agent
Shows agent in action with mock data (no API key needed)
Run: python demo.py
"""

from agent import create_agent
import os

def demo():
    """Run demo with mock data"""
    
    print("\n" + "█"*70)
    print("█  RESEARCH ASSISTANT AGENT - DEMO")
    print("█"*70)
    print("█  This demo uses MOCK DATA (no API key needed)")
    print("█  Set USE_MOCK=False in main.py for real web search")
    print("█"*70 + "\n")
    
    # Create agent in mock mode
    agent = create_agent(log_level='INFO', use_mock=True)
    
    # Example topic
    topic = "renewable energy climate change"
    
    print(f"Researching: '{topic}'")
    print("Running agent workflow...\n")
    
    # Run agent
    try:
        report = agent.run(topic)
        
        # Save report with UTF-8 encoding (fixes Windows encoding issues)
        os.makedirs('output', exist_ok=True)
        output_file = os.path.join('output', 'demo_report.md')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Display results
        print("\n" + "="*70)
        print("GENERATED REPORT")
        print("="*70)
        print(report)
        
        print("\n" + "="*70)
        print("EXECUTION STATISTICS")
        print("="*70)
        summary = agent.get_state_summary()
        for key, value in summary.items():
            print(f"  {key:.<40} {value}")
        
        # Show log entries
        logs = agent.get_execution_log()
        print(f"\n  Log entries:.......................... {len(logs)}")
        
        # Show any errors
        errors = agent.get_errors()
        if errors:
            print(f"  Errors:.............................. {len(errors)}")
            for error in errors[:3]:
                print(f"    - {error['error_type']}: {error['message']}")
        else:
            print(f"  Errors:.............................. 0 ✓")
        
        print(f"\n✓ Report saved to: {output_file}")
        print("="*70 + "\n")
        
        # Success
        return True
    
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = demo()
    exit(0 if success else 1)
