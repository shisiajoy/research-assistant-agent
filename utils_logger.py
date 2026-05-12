"""
utils/logger.py - Logging configuration and utilities
Sets up structured logging for the agent
"""

import logging
import os
from datetime import datetime
from typing import Optional

# ============================================================================
# LOGGER SETUP
# ============================================================================

def setup_logger(name: str = 'research_agent', log_level: str = 'INFO') -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name (appears in logs)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs', exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    # Avoid duplicate handlers
    if logger.hasHandlers():
        return logger
    
    # Create formatters
    file_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)-8s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        fmt='%(levelname)-8s | %(name)s | %(message)s'
    )
    
    # File handler - logs everything
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_handler = logging.FileHandler(f'logs/research_agent_{timestamp}.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler - logs INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = 'research_agent') -> logging.Logger:
    """Get existing logger or create new one"""
    return logging.getLogger(name)


# ============================================================================
# CUSTOM LOGGING FUNCTIONS
# ============================================================================

def log_node_entry(logger: logging.Logger, node_name: str, state_summary: dict):
    """Log entering a node"""
    logger.info(f"{'='*60}")
    logger.info(f"ENTERING: {node_name}")
    logger.info(f"State summary: {state_summary}")
    logger.info(f"{'='*60}")


def log_node_exit(logger: logging.Logger, node_name: str, success: bool, message: str = ""):
    """Log exiting a node"""
    status = "✓ SUCCESS" if success else "✗ FAILED"
    logger.info(f"EXITING: {node_name} - {status} {message}")
    logger.info(f"{'-'*60}\n")


def log_tool_call(logger: logging.Logger, tool_name: str, **kwargs):
    """Log tool invocation"""
    args_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
    logger.debug(f"Tool call: {tool_name}({args_str})")


def log_tool_result(logger: logging.Logger, tool_name: str, result: dict):
    """Log tool result"""
    result_str = ", ".join([f"{k}={v}" for k, v in result.items()])
    logger.debug(f"Tool result: {tool_name} -> {result_str}")


# ============================================================================
# PROGRESS TRACKING
# ============================================================================

class ProgressTracker:
    """Track progress through workflow"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.current_step = 0
        self.total_steps = 0
        self.steps = []
    
    def set_total_steps(self, total: int):
        """Set total number of steps"""
        self.total_steps = total
    
    def add_step(self, name: str):
        """Register a named step"""
        self.steps.append(name)
    
    def start_step(self, step_name: str):
        """Mark step as started"""
        self.current_step += 1
        percent = (self.current_step / self.total_steps * 100) if self.total_steps > 0 else 0
        self.logger.info(f"[{self.current_step}/{self.total_steps}] {percent:.0f}% - {step_name}")
    
    def complete_step(self):
        """Mark step as completed"""
        pass  # Could add more tracking here


if __name__ == "__main__":
    # Test logger
    logger = setup_logger(log_level='DEBUG')
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    print("✓ Logger test complete - check logs/ folder")
