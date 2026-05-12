# Research Assistant Agent 🤖

An autonomous AI research agent that automatically researches topics, fetches from multiple sources, synthesizes findings, and generates comprehensive reports.


## 🎯 Overview

This is a complete multi-agent system that demonstrates autonomous research automation. The agent:

1. Parses your research topic and extracts keywords
2. Searches multiple sources using NewsAPI
3. Analyzes findings and detects conflicts
4. Generates professional markdown reports with citations

   
This design reflects modern **agent-based architectures** used in real-world AI systems, where tasks are broken into specialized steps rather than handled by a single model.


Key Features

✅ Autonomous Workflow - 4-node agent system with state management

✅ Real API Integration - Uses NewsAPI to fetch actual articles

✅ Smart Analysis - Extracts claims, scores credibility, detects conflicts

✅ Professional Reports - Generates markdown with proper citations

✅ Error Handling - Graceful degradation if API fails

✅ Full Logging - Tracks every step of execution

✅ Production Ready - Complete documentation and error recovery


---

## 📊 System Architecture

INPUT: Research Topic
  ↓
[NODE 1] Parse Topic
  └─ Extract keywords & subtopics
  ↓
[NODE 2] Multi-Source Search
  └─ Search NewsAPI + Fetch content
  ↓
[NODE 3] Analyze & Synthesize
  └─ Extract claims + Score confidence
  ↓
[NODE 4] Generate Report
  └─ Create markdown with citations
  ↓
OUTPUT: Comprehensive Research Report (Markdown)


## 📊 Features & Capabilities
Node 1: Parse Topic ✅

Extract keywords from research topic
Identify subtopics
Create search strategy
Example: "Benefits of renewable energy" → ["benefits", "renewable", "energy"]

Node 2: Multi-Source Search ✅

Search NewsAPI for articles
Fetch and parse content
Score source credibility
Handle API failures gracefully
Result: 10-20 sources with credibility scores

Node 3: Analyze & Synthesize ✅

Extract key claims from sources
Calculate confidence scores
Detect conflicting information
Categorize findings by topic
Result: 20-30 synthesized findings

Node 4: Generate Report ✅

Organize findings by category
Create proper citations
Format as professional markdown
Add execution statistics
Result: publication-ready markdown report



## 🛠️ Tech Stack

Python

OpenAI API

Requests

dotenv


## 🛠️ Dependencies

1.requests version 2.33.1 - purpose HTTP requests to NewsAPI

2.beautifulsoup version 44.14.3 - purpose HTML parsing & content extraction

3.lxm version l6.1.0 - purpose Fast XML/HTML parser

4.nltk version 3.9.4 - purpose Natural language processing

5.python-dotenv version 1.2.2 - purpose Environment variable management


Install all: pip install -r requirements.txt

