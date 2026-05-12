"""
utils/error_handler.py - Custom exceptions and error handling
Defines all custom error types for the agent
"""

# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class ResearchAgentError(Exception):
    """Base exception for Research Assistant Agent"""
    pass


class SearchError(ResearchAgentError):
    """Failed to perform web search"""
    pass


class FetchError(ResearchAgentError):
    """Failed to fetch or parse web content"""
    pass


class NoSourcesFoundError(ResearchAgentError):
    """No sources found for research topic"""
    pass


class CredibilityScoreError(ResearchAgentError):
    """Failed to calculate credibility score"""
    pass


class SynthesisError(ResearchAgentError):
    """Failed during synthesis phase"""
    pass


class ReportGenerationError(ResearchAgentError):
    """Failed to generate report"""
    pass


class InvalidInputError(ResearchAgentError):
    """Invalid input provided to agent"""
    pass


class APIError(ResearchAgentError):
    """External API error"""
    pass


class TimeoutError(ResearchAgentError):
    """Request timed out"""
    pass


class NetworkError(ResearchAgentError):
    """Network connectivity issue"""
    pass


# ============================================================================
# ERROR HANDLING UTILITIES
# ============================================================================

class ErrorHandler:
    """Utility for handling errors gracefully"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.errors = []
    
    def handle(self, error: Exception, context: str, recoverable: bool = True) -> dict:
        """
        Handle an error and return error info.
        
        Args:
            error: The exception that occurred
            context: Where the error occurred (e.g., "fetching URL")
            recoverable: Whether execution can continue
        
        Returns:
            Dictionary with error info
        """
        import traceback
        
        error_info = {
            'error_type': type(error).__name__,
            'message': str(error),
            'context': context,
            'recoverable': recoverable,
            'stacktrace': traceback.format_exc()
        }
        
        self.errors.append(error_info)
        
        if self.logger:
            level = 'warning' if recoverable else 'error'
            getattr(self.logger, level)(
                f"[{context}] {type(error).__name__}: {error} "
                f"(recoverable: {recoverable})"
            )
        
        return error_info
    
    def get_errors(self):
        """Get all handled errors"""
        return self.errors
    
    def get_error_count(self):
        """Get number of errors"""
        return len(self.errors)
    
    def had_fatal_error(self):
        """Check if any unrecoverable errors occurred"""
        return any(not e['recoverable'] for e in self.errors)


# ============================================================================
# ERROR RECOVERY STRATEGIES
# ============================================================================

def safe_call(func, *args, default=None, error_handler=None, context="function call", **kwargs):
    """
    Safely call a function with error handling.
    
    Args:
        func: Function to call
        args: Positional arguments
        default: Default return value on error
        error_handler: ErrorHandler instance
        context: Context string for logging
        kwargs: Keyword arguments
    
    Returns:
        Function result or default value
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if error_handler:
            error_handler.handle(e, context, recoverable=True)
        return default


def retry_with_backoff(func, max_retries=3, backoff_factor=2, *args, **kwargs):
    """
    Retry a function with exponential backoff.
    
    Args:
        func: Function to call
        max_retries: Maximum number of attempts
        backoff_factor: Multiplier for backoff delay
        args, kwargs: Arguments to pass to function
    
    Returns:
        Function result or raises exception after max retries
    """
    import time
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Last attempt, raise the error
            
            # Wait before retry (exponential backoff)
            wait_time = backoff_factor ** attempt
            time.sleep(wait_time)
    
    return None
