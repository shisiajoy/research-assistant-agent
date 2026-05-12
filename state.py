"""
state.py - Data structures for Research Assistant Agent
Defines all state objects that flow through the agent workflow
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any

# ============================================================================
# CORE STATE OBJECTS
# ============================================================================

@dataclass
class Source:
    """Represents a single source found during search"""
    url: str
    title: str
    content: str
    credibility_score: float = 0.5  # 0-1 scale
    fetch_timestamp: datetime = field(default_factory=datetime.now)
    fetch_status: str = "success"  # success, timeout, error, invalid
    domain: str = ""
    author: Optional[str] = None
    publish_date: Optional[str] = None
    
    def __str__(self):
        return f"Source(title='{self.title}', credibility={self.credibility_score:.2f})"


@dataclass
class Finding:
    """Represents a synthesized finding from sources"""
    claim: str
    supporting_sources: List[int] = field(default_factory=list)  # indices into raw_sources
    confidence: float = 0.5
    conflicts: List[str] = field(default_factory=list)
    topic_category: str = "General"
    evidence_count: int = 0
    
    def __str__(self):
        return f"Finding('{self.claim[:50]}...', confidence={self.confidence:.1%})"


@dataclass
class LogEntry:
    """Single log entry"""
    timestamp: datetime = field(default_factory=datetime.now)
    level: str = "INFO"  # INFO, WARNING, ERROR, DEBUG
    component: str = ""  # which node/component
    message: str = ""
    context: Optional[Dict[str, Any]] = None
    
    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.level:8} | {self.component:20} | {self.message}"


@dataclass
class ErrorRecord:
    """Track errors during execution"""
    timestamp: datetime = field(default_factory=datetime.now)
    error_type: str = ""
    message: str = ""
    context: str = ""  # where did it happen
    stacktrace: str = ""
    is_recoverable: bool = True
    
    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.error_type}: {self.message} ({self.context})"


@dataclass
class SearchStrategy:
    """Strategy for searching based on topic"""
    primary_keywords: List[str] = field(default_factory=list)
    secondary_keywords: List[str] = field(default_factory=list)
    subtopics: List[str] = field(default_factory=list)
    search_depth: int = 3  # 1=shallow, 2=medium, 3=deep
    max_sources: int = 10
    exclude_terms: List[str] = field(default_factory=list)


@dataclass
class ReportMetadata:
    """Metadata about generated report"""
    generated_at: str = ""
    sources_count: int = 0
    findings_count: int = 0
    average_confidence: float = 0.0
    high_confidence_findings: int = 0
    conflicting_claims_count: int = 0
    execution_time_seconds: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            'generated_at': self.generated_at,
            'sources_count': self.sources_count,
            'findings_count': self.findings_count,
            'average_confidence': f"{self.average_confidence:.1%}",
            'high_confidence_findings': self.high_confidence_findings,
            'conflicting_claims_count': self.conflicting_claims_count,
            'execution_time_seconds': f"{self.execution_time_seconds:.2f}s"
        }


# ============================================================================
# MAIN STATE CLASS
# ============================================================================

@dataclass
class ResearchState:
    """
    Complete state object that flows through all nodes.
    Each node reads from and writes to this state.
    """
    
    # -------- INITIAL INPUT --------
    research_topic: str = ""
    user_context: str = ""  # Additional context from user
    
    # -------- NODE 1: PARSE TOPIC --------
    search_keywords: List[str] = field(default_factory=list)
    subtopics: List[str] = field(default_factory=list)
    search_strategy: Optional[SearchStrategy] = None
    
    # -------- NODE 2: SEARCH --------
    raw_sources: List[Source] = field(default_factory=list)
    sources_searched: int = 0
    sources_failed: int = 0
    
    # -------- NODE 3: SYNTHESIZE --------
    synthesized_findings: List[Finding] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)  # Main themes found
    
    # -------- NODE 4: REPORT --------
    final_report: str = ""
    report_metadata: Optional[ReportMetadata] = None
    
    # -------- EXECUTION TRACKING --------
    execution_log: List[LogEntry] = field(default_factory=list)
    errors: List[ErrorRecord] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    # -------- NODE EXECUTION STATUS --------
    nodes_completed: List[str] = field(default_factory=list)
    current_node: str = ""
    
    def add_log(self, level: str, component: str, message: str, context: Optional[Dict] = None):
        """Add entry to execution log"""
        entry = LogEntry(
            timestamp=datetime.now(),
            level=level,
            component=component,
            message=message,
            context=context
        )
        self.execution_log.append(entry)
    
    def add_error(self, error_type: str, message: str, context: str, stacktrace: str = "", recoverable: bool = True):
        """Add error record"""
        error = ErrorRecord(
            timestamp=datetime.now(),
            error_type=error_type,
            message=message,
            context=context,
            stacktrace=stacktrace,
            is_recoverable=recoverable
        )
        self.errors.append(error)
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Return summary of execution"""
        return {
            'topic': self.research_topic,
            'sources_found': len(self.raw_sources),
            'findings_synthesized': len(self.synthesized_findings),
            'errors_encountered': len(self.errors),
            'nodes_completed': self.nodes_completed,
            'log_entries': len(self.execution_log)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary (for serialization)"""
        return {
            'research_topic': self.research_topic,
            'keywords': self.search_keywords,
            'subtopics': self.subtopics,
            'sources_found': len(self.raw_sources),
            'findings': len(self.synthesized_findings),
            'execution_logs': len(self.execution_log),
            'errors': len(self.errors),
            'nodes_completed': self.nodes_completed
        }


# ============================================================================
# CONSTANTS
# ============================================================================

DEFAULT_SEARCH_DEPTH = 3
DEFAULT_MAX_SOURCES = 10
MIN_CREDIBILITY_SCORE = 0.0
MAX_CREDIBILITY_SCORE = 1.0
CONFIDENCE_THRESHOLD_HIGH = 0.75
CONFIDENCE_THRESHOLD_MEDIUM = 0.50
