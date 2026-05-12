# Research Assistant Agent - Architecture & Design Documentation

## Project Overview

End-to-end AI agent that researches topics by:
1. Parsing user input → extract keywords
2. Searching multiple sources → fetch content
3. Analyzing findings → synthesize insights
4. Generating report → formatted markdown with citations

## Workflow Architecture

```
INPUT: Research Topic
    ↓
NODE 1: Parse Topic
    - Extract keywords
    - Identify subtopics
    - Create search strategy
    ↓
NODE 2: Multi-Source Search
    - Search web (NewsAPI or mock)
    - Fetch article content
    - Score source credibility
    ↓
NODE 3: Analyze & Synthesize
    - Extract key claims
    - Detect conflicts
    - Categorize findings
    - Identify themes
    ↓
NODE 4: Generate Report
    - Organize by category
    - Create citations
    - Add confidence scores
    - Output markdown
    ↓
OUTPUT: Research Report (Markdown)
```

## State Management

Single `ResearchState` object flows through all nodes:

```python
ResearchState:
  - research_topic (str)
  - search_keywords (List[str])
  - raw_sources (List[Source])
  - synthesized_findings (List[Finding])
  - final_report (str)
  - execution_log (List[LogEntry])
  - errors (List[ErrorRecord])
```

## File Structure

```
research_agent_capstone/
├── venv/                      # Virtual environment
├── requirements.txt           # Python dependencies
├── SETUP_GUIDE.md            # Installation & setup
├── .env.example              # API key template
│
├── agent.py                  # Main orchestrator (ResearchAgent class)
├── main.py                   # Entry point - modify RESEARCH_TOPIC here
├── demo.py                   # Demo with mock data
│
├── state.py                  # Data structures
├── nodes_all.py              # Workflow nodes (Node1-4)
├── tools_all.py              # Tools (search, fetch, credibility, citations)
├── utils_logger.py           # Logging setup
├── utils_error_handler.py    # Error handling
│
├── output/                   # Generated reports
│   └── research_report_*.md
│
└── logs/                     # Execution logs
    └── research_agent_*.log
```

## Core Components

### agent.py - ResearchAgent Class
- Coordinates all nodes
- Manages state throughout workflow
- Error handling & recovery
- Report generation and saving
- Execution logging

### state.py - Data Structures
- `ResearchState`: Main state container
- `Source`: Found article/source
- `Finding`: Synthesized finding with confidence
- `LogEntry`: Execution log
- `ErrorRecord`: Error tracking

### nodes_all.py - Workflow Implementation
- **Node1**: Parse topic → keywords
- **Node2**: Search web → fetch content
- **Node3**: Analyze sources → synthesize findings
- **Node4**: Generate → markdown report

### tools_all.py - Tool Implementations
- **SearchTool**: NewsAPI search (or mock)
- **FetchTool**: HTML parsing & content extraction
- **CredibilityTool**: Source credibility scoring
- **CitationTool**: Formatted citations

## Design Decisions

### Sequential Nodes (Not Parallel)
- Each node depends on previous output
- Simpler error handling
- Clear state progression
- Better for learning

### Credibility Scoring
- Domain reputation (trusted sites = higher score)
- HTTPS verification
- Content analysis (length, citations)
- Range: 0.0 (unreliable) to 1.0 (highly reliable)

### Error Handling Strategy
- Try-except around all external calls
- Recoverable errors → continue with fallback
- Non-recoverable errors → attempt graceful degradation
- All errors logged for debugging
- Report generation succeeds even with partial data

### Mock Data Mode
- Simulates search results & web pages
- No API key required
- Identical workflow to real mode
- Perfect for testing & learning

## Key Features

✓ Multi-step workflow (4 nodes)
✓ Tool integration (5 tools)
✓ State management (ResearchState flows through)
✓ Error handling (try-except + recovery)
✓ Logging/observability (file + console)
✓ Working demo (no API needed)
✓ Full documentation

## Dependencies

| Package | Purpose |
|---------|---------|
| requests | HTTP requests |
| beautifulsoup4 | HTML parsing |
| lxml | XML/HTML backend |
| nltk | Text processing |
| newsapi | News search API |
| python-dotenv | Environment variables |

## Running the Agent

### Demo (No API Key Needed)
```bash
python demo.py
```

### With Your Topic
Edit `main.py` line 11:
```python
RESEARCH_TOPIC = "Your topic here"
```
Then:
```bash
python main.py
```

### With Real API (Optional)
1. Get free API key: https://newsapi.org/
2. Create `.env` file with: `NEWSAPI_KEY=your_key`
3. Set `USE_MOCK_DATA = False` in main.py
4. Run: `python main.py`

## Output Files

- `output/research_report_*.md` - Generated reports
- `logs/research_agent_*.log` - Execution logs

## Challenges & Solutions

### Challenge: API Rate Limiting
**Solution:** Mock data fallback, retry with backoff

### Challenge: Conflicting Information
**Solution:** Flag conflicting claims, show all sources, allow users to evaluate

### Challenge: Content Quality
**Solution:** Credibility scoring, content extraction filtering, confidence indicators

### Challenge: Execution Time
**Solution:** Demo mode for fast testing, parallel search possible (future)

## Future Improvements

1. Parallel source searching (faster execution)
2. Semantic similarity for deduplication (better accuracy)
3. NLP summary generation (automatic summaries)
4. Academic database integration (more sources)
5. Web UI (easier to use)
6. Caching mechanism (repeated queries)
7. Multi-language support
8. Advanced NLP analysis (topic modeling, entity extraction)

## Testing the System

### Quick Test (30 seconds)
```bash
python demo.py
```
Check: `output/demo_report.md`

### Full Test
```bash
python main.py
```
Check: `output/research_report_*.md`

### Debug Mode
Change in agent.py:
```python
self.logger = setup_logger('research_agent', 'DEBUG')
```

## Key Metrics

- **Sources found**: Count of articles/sources
- **Findings synthesized**: Count of extracted claims
- **Average confidence**: Weighted confidence score
- **Conflicting claims**: Number of contradictions found
- **Execution time**: Total time to complete

## Important Notes

- First run downloads NLTK data (~100MB) - may take time
- Mock mode always works, no internet required
- Real mode needs internet connection
- Reports saved to `output/` folder
- Logs saved to `logs/` folder
- All errors logged but don't stop execution
- Can handle partial data (graceful degradation)

## Rubric Alignment

✓ Multi-step workflow (Nodes 1-4)
✓ Tool integration (Search, Fetch, Credibility, Citations)
✓ State management (ResearchState with clear data flow)
✓ Error handling (Try-except, recovery strategies)
✓ Logging/observability (Comprehensive logging at each step)
✓ Working demonstration (demo.py with no API needed)
✓ Documentation (This file + SETUP_GUIDE.md)

---

**For Implementation Guide:** See SETUP_GUIDE.md
**For Setup & Installation:** See SETUP_GUIDE.md
**For Quick Start:** Run `python demo.py`
