"""
agent.py - Main Research Assistant Agent orchestrator
Coordinates all workflow nodes and state management
"""

import os
from datetime import datetime
from state import ResearchState, ReportMetadata
from nodes_all import Node1ParseTopic, Node2Search, Node3Synthesize, Node4Report
from utils_logger import setup_logger, get_logger
from utils_error_handler import ErrorHandler, ResearchAgentError
import logging

# ============================================================================
# RESEARCH AGENT
# ============================================================================

class ResearchAgent:
    """
    Main research agent that orchestrates the workflow.
    Manages state, coordinates nodes, handles errors.
    """
    
    def __init__(self, log_level: str = 'INFO', use_mock: bool = False):
        """
        Initialize the research agent.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
            use_mock: Use mock data instead of real API calls
        """
        self.state = ResearchState()
        self.error_handler = ErrorHandler(logger=None)
        self.logger = setup_logger('research_agent', log_level)
        self.use_mock = use_mock
        self.start_time = None
        self.end_time = None
    
    def run(self, research_topic: str) -> str:
        """
        Execute the complete research workflow.
        
        Args:
            research_topic: The topic to research
        
        Returns:
            Final research report as markdown string
        """
        try:
            self.start_time = datetime.now()
            self.logger.info("\n" + "="*70)
            self.logger.info("RESEARCH ASSISTANT AGENT - START")
            self.logger.info("="*70)
            self.logger.info(f"Topic: {research_topic}")
            self.logger.info("="*70 + "\n")
            
            # Set initial state
            self.state.research_topic = research_topic
            self.state.start_time = self.start_time
            
            # Execute workflow nodes
            if not self._execute_node(Node1ParseTopic):
                raise ResearchAgentError("Failed at Node 1: Parse Topic")
            
            if not self._execute_node(Node2Search):
                self.logger.warning("Node 2 failed - attempting to continue with Node 3...")
            
            if not self._execute_node(Node3Synthesize):
                self.logger.warning("Node 3 failed - generating report with available data...")
            
            if not self._execute_node(Node4Report):
                raise ResearchAgentError("Failed at Node 4: Report Generation")
            
            self.end_time = datetime.now()
            self.state.end_time = self.end_time
            
            # Calculate execution time
            execution_time = (self.end_time - self.start_time).total_seconds()
            if self.state.report_metadata:
                self.state.report_metadata.execution_time_seconds = execution_time
            
            self._print_summary()
            
            self.logger.info("\n" + "="*70)
            self.logger.info("RESEARCH ASSISTANT AGENT - COMPLETE ✓")
            self.logger.info("="*70)
            self.logger.info(f"Total execution time: {execution_time:.2f} seconds")
            self.logger.info(f"Report saved to: research_report.md")
            self.logger.info("="*70 + "\n")
            
            return self.state.final_report
        
        except ResearchAgentError as e:
            self.logger.error(f"\n✗ RESEARCH FAILED: {e}")
            return self._generate_fallback_report()
        except Exception as e:
            self.logger.error(f"\n✗ UNEXPECTED ERROR: {e}")
            self.error_handler.handle(e, "main workflow", recoverable=False)
            return self._generate_fallback_report()
    
    def _execute_node(self, node_class) -> bool:
        """
        Execute a single workflow node.
        
        Args:
            node_class: Node class to execute (Node1, Node2, etc.)
        
        Returns:
            Success boolean
        """
        try:
            return node_class.execute(self.state, self.error_handler)
        except Exception as e:
            self.logger.error(f"Node execution error: {e}")
            self.error_handler.handle(e, f"{node_class.__name__}", recoverable=True)
            return False
    
    def _print_summary(self):
        """Print execution summary"""
        self.logger.info("\n" + "-"*70)
        self.logger.info("EXECUTION SUMMARY")
        self.logger.info("-"*70)
        
        summary = self.state.get_execution_summary()
        for key, value in summary.items():
            self.logger.info(f"  {key:.<40} {value}")
        
        if self.state.report_metadata:
            meta = self.state.report_metadata.to_dict()
            self.logger.info("\nREPORT METADATA:")
            for key, value in meta.items():
                self.logger.info(f"  {key:.<40} {value}")
        
        if self.error_handler.get_errors():
            self.logger.warning(f"\nErrors encountered: {self.error_handler.get_error_count()}")
            for error in self.error_handler.get_errors()[-3:]:  # Last 3 errors
                self.logger.warning(f"  - {error['error_type']}: {error['message']}")
        
        self.logger.info("-"*70)
    
    def _generate_fallback_report(self) -> str:
        """Generate minimal report if workflow fails"""
        report = f"# {self.state.research_topic}\n\n"
        report += "*Report generation failed due to errors.*\n\n"
        
        if self.state.raw_sources:
            report += "## Sources Found\n\n"
            for source in self.state.raw_sources:
                report += f"- [{source.title}]({source.url})\n"
        
        if self.state.synthesized_findings:
            report += "\n## Partial Findings\n\n"
            for finding in self.state.synthesized_findings:
                report += f"- {finding.claim}\n"
        
        report += "\n---\n"
        report += f"\nExecution errors: {len(self.state.errors)}\n"
        
        return report
    
    def save_report(self, filename: str = None):
        """
        Save report to file.
        
        Args:
            filename: Output filename (default: research_report.md)
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            topic_slug = self.state.research_topic.replace(' ', '_')[:30]
            filename = f"research_report_{topic_slug}_{timestamp}.md"
        
        # Ensure output directory exists
        os.makedirs('output', exist_ok=True)
        filepath = os.path.join('output', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.state.final_report)
        
        self.logger.info(f"Report saved to: {filepath}")
        return filepath
    
    def get_state_summary(self) -> dict:
        """Get current state summary"""
        return self.state.get_execution_summary()
    
    def get_execution_log(self) -> list:
        """Get execution log entries"""
        return self.state.execution_log
    
    def get_errors(self) -> list:
        """Get error records"""
        return self.state.errors


# ============================================================================
# AGENT FACTORY
# ============================================================================

def create_agent(log_level: str = 'INFO', use_mock: bool = False) -> ResearchAgent:
    """
    Factory function to create a research agent.
    
    Args:
        log_level: Logging level
        use_mock: Use mock data
    
    Returns:
        Configured ResearchAgent instance
    """
    return ResearchAgent(log_level=log_level, use_mock=use_mock)


if __name__ == "__main__":
    # Quick test
    agent = create_agent(log_level='INFO')
    report = agent.run("The impact of renewable energy on climate change")
    
    print("\n" + "="*70)
    print("SAMPLE OUTPUT:")
    print("="*70)
    print(report[:500] + "\n...\n")
    
    agent.save_report()
