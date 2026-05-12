# Research Assistant Agent - Complete Setup & Implementation Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Project Structure](#project-structure)
4. [Dependencies Explained](#dependencies-explained)
5. [API Setup](#api-setup)
6. [Running the Agent](#running-the-agent)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements:
- **Python**: 3.9 or higher (3.10+ recommended)
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB for dependencies
- **Internet Connection**: Required for web search functionality

### Check Your Python Version:
```bash
python --version
# or
python3 --version
```

If you don't have Python installed, download from: https://www.python.org/downloads/

---

## Installation Steps

### Step 1: Create a Project Folder
Create a dedicated folder for this project on your computer:

```bash
# Navigate to where you want the project
cd Desktop
mkdir research_agent_capstone
cd research_agent_capstone
```

### Step 2: Create Virtual Environment (HIGHLY RECOMMENDED)

A virtual environment isolates project dependencies from your system Python.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line when activated.

### Step 3: Install Dependencies

Download the `requirements.txt` file into your project folder, then run:

```bash
pip install -r requirements.txt
```

**What this does:**
- Downloads all required Python packages
- Installs them into your virtual environment
- May take 2-5 minutes depending on internet speed

### Step 4: Verify Installation

Test that everything is installed correctly:

```bash
python -c "import requests; import bs4; import nltk; print('✓ All dependencies installed successfully!')"
```

---

## Project Structure

Once you've set everything up, your project folder should look like this:

```
research_agent_capstone/
│
├── venv/                          # Virtual environment (created automatically)
│
├── requirements.txt               # Dependencies list
├── SETUP_GUIDE.md                # This file
│
├── main.py                       # Entry point - START HERE
├── demo.py                       # Runnable demonstration
├── agent.py                      # Core agent orchestration
├── state.py                      # Data structures & state management
│
├── nodes/                        # Workflow nodes
│   ├── __init__.py
│   ├── node1_parse_topic.py
│   ├── node2_search.py
│   ├── node3_synthesize.py
│   └── node4_report.py
│
├── tools/                        # Tool implementations
│   ├── __init__.py
│   ├── search_tool.py
│   ├── fetch_tool.py
│   ├── credibility.py
│   └── citations.py
│
├── utils/                        # Utilities
│   ├── __init__.py
│   ├── logger.py
│   └── error_handler.py
│
├── logs/                         # Created automatically
│   └── research_agent.log
│
└── output/                       # Generated reports
    └── report_*.md
```

---

## Dependencies Explained

### Core Libraries:

| Package | Version | Purpose | Why Needed |
|---------|---------|---------|-----------|
| **requests** | 2.31.0 | HTTP requests | Fetch web pages and call APIs |
| **beautifulsoup4** | 4.12.2 | HTML parsing | Extract text from web pages |
| **lxml** | 4.9.3 | XML/HTML parser | Backend for BeautifulSoup (faster) |
| **nltk** | 3.8.1 | NLP tools | Extract sentences, tokenize text, remove stopwords |
| **newsapi** | 0.1.1 | News API wrapper | Search news articles (optional - can be mocked) |
| **python-dateutil** | 2.8.2 | Date handling | Parse timestamps from articles |
| **python-dotenv** | 1.0.0 | Environment variables | Load API keys from .env file |
| **numpy** | 1.24.3 | Numerical computing | Calculate statistics (confidence scores) |
| **colorama** | 0.4.6 | Colored terminal output | Better logging readability (optional) |

### Why Each Is Important:

- **requests + beautifulsoup4 + lxml**: Core web scraping stack
- **nltk**: Advanced text processing (sentence extraction, stemming)
- **newsapi**: NewsAPI integration for searching articles
- **python-dotenv**: Secure API key management
- **numpy**: Statistical calculations for confidence scores

---

## API Setup (Optional but Recommended)

### Using NewsAPI (Free Plan Available)

For real web search functionality, you can use NewsAPI:

1. **Get a Free API Key:**
   - Visit: https://newsapi.org/
   - Click "Register"
   - Create account with email
   - Copy your API key

2. **Create .env file:**
   In your project folder, create a file named `.env`:
   
   ```
   NEWSAPI_KEY=your_api_key_here_paste_it
   ```
   
   Example:
   ```
   NEWSAPI_KEY=abc123def456ghi789jkl012mno345
   ```

3. **Alternative: Use Mock Data (No API Key Needed)**
   
   The code includes a mock mode that simulates API responses without needing a real API key. This is perfect for testing and learning!
   
   To use mock mode, simply don't provide an API key in `.env`.

---

## Running the Agent

### Option 1: Run the Demo (Recommended First)

The demo shows the agent in action with example data:

```bash
python demo.py
```

**Expected output:**
- Agent starts processing a sample research topic
- Shows execution logs
- Generates a markdown report
- Saves to `output/` folder

### Option 2: Run with Custom Topic

Edit `main.py` and change the topic:

```python
if __name__ == "__main__":
    # Change this to your research topic
    topic = "Your Research Topic Here"
    agent = ResearchAgent()
    report = agent.run(topic)
```

Then run:
```bash
python main.py
```

### Option 3: Interactive Mode (Advanced)

Create a file called `interactive.py`:

```python
from agent import ResearchAgent

if __name__ == "__main__":
    agent = ResearchAgent()
    
    topic = input("Enter your research topic: ")
    print(f"\nResearching: {topic}")
    print("This may take 30-60 seconds...\n")
    
    report = agent.run(topic)
    
    # Save report
    filename = f"output/report_{topic.replace(' ', '_')[:50]}.md"
    with open(filename, 'w') as f:
        f.write(report)
    
    print(f"\n✓ Report saved to: {filename}")
    print("\nReport preview:")
    print(report[:500] + "...")
```

Run it:
```bash
python interactive.py
```

---

## Detailed File Descriptions

### main.py
- **Purpose**: Entry point of the application
- **What it does**: Imports the agent and runs it with a test topic
- **When to modify**: Change the research topic here for testing

### demo.py
- **Purpose**: Demonstrates the agent with example data
- **What it does**: Runs agent with mock data and shows logging
- **When to run**: First thing - test the system is working
- **No API needed**: Uses simulated data

### agent.py
- **Purpose**: Core orchestration logic
- **Size**: ~400 lines
- **Key classes**: `ResearchAgent`
- **Key methods**: `run()`, `_node1_parse_topic()`, `_node2_search()`, etc.

### state.py
- **Purpose**: Data structures that hold state
- **Key classes**: 
  - `ResearchState`: Main state object
  - `Source`: Represents a found source
  - `Finding`: A synthesized finding
  - `LogEntry`: Execution log
  - `ErrorRecord`: Error tracking

### nodes/ folder
Each file implements one workflow step:

- **node1_parse_topic.py**: Parse input and extract keywords
- **node2_search.py**: Search sources and fetch content
- **node3_synthesize.py**: Analyze and synthesize findings
- **node4_report.py**: Generate formatted report

### tools/ folder
Implementations of tools the agent uses:

- **search_tool.py**: Search functionality (NewsAPI or mock)
- **fetch_tool.py**: Fetch and parse web content
- **credibility.py**: Score source credibility
- **citations.py**: Format citations

### utils/ folder
Helper utilities:

- **logger.py**: Logging setup
- **error_handler.py**: Custom exception classes

---

## Running Tests

### Quick Test (30 seconds):
```bash
python demo.py
```

### Full Test Suite (if you add tests):
```bash
pytest tests/ -v
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'requests'"

**Solution:**
1. Make sure your virtual environment is activated (should see `(venv)` in terminal)
2. Run: `pip install requests`
3. Or reinstall everything: `pip install -r requirements.txt`

### Problem: "Python version 3.8 not supported"

**Solution:**
Install Python 3.9+: https://www.python.org/downloads/
Then recreate virtual environment with new Python version.

### Problem: "No module named 'nltk'"

**Solution:**
```bash
pip install nltk
python -c "import nltk; nltk.download('punkt')"
```

### Problem: Web pages not fetching / API errors

**Solution:**
1. Check internet connection
2. The code has built-in fallback to mock data
3. Run `demo.py` which uses mock data
4. Check `logs/research_agent.log` for details

### Problem: "FileNotFoundError: output directory"

**Solution:**
The code creates the output folder automatically. If it doesn't:
```bash
mkdir output
mkdir logs
```

### Problem: Windows permission error on venv activation

**Solution:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Takes too long to run

**Solution:**
- Demo mode is faster (uses mock data)
- Real mode fetches actual web pages (slower)
- Network speed affects performance
- Check `logs/research_agent.log` to see progress

---

## Performance Tips

1. **Use demo mode first**: `python demo.py` (instant)
2. **Set max_results lower** in node2_search.py if slow
3. **Run during off-peak hours** for faster web access
4. **Use mock data mode** if API rate-limited

---

## Next Steps After Installation

1. ✅ Verify Python installation
2. ✅ Create virtual environment
3. ✅ Install dependencies
4. ✅ Run `python demo.py`
5. ✅ Check generated reports in `output/` folder
6. ✅ Review logs in `logs/research_agent.log`
7. ✅ Modify agent for your research topic
8. ✅ Run main.py with custom topic

---

## Getting Help

If something doesn't work:

1. **Check the logs**: Open `logs/research_agent.log`
2. **Run in demo mode**: `python demo.py` (no API needed)
3. **Print state**: Add `print(agent.state.__dict__)` to debug
4. **Check Python version**: `python --version` must be 3.9+
5. **Verify venv is active**: Should see `(venv)` in terminal

---

## Project Structure Quick Reference

```
START HERE:
  1. python demo.py              # Test with mock data
  2. python main.py              # Run with default topic
  3. Modify main.py with your topic
  4. Check output/ folder for generated reports
  5. Review logs/research_agent.log for execution details
```
