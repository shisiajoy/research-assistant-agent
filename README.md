# 🧠 Research Assistant Agent

An intelligent, multi-step AI system that automates research workflows — from query understanding to structured report generation.


## 🚀 Overview

This agent implements a **multi-node AI agent pipeline** that mimics how real research is done:

1. Understand the query  
2. Search for information  
3. Extract key insights  
4. Generate a structured report  

This design reflects modern **agent-based architectures** used in real-world AI systems, where tasks are broken into specialized steps rather than handled by a single model. :contentReference[oaicite:0]{index=0}  

---

## 🏗️ Architecture


User Query
↓
[Node 1] Parse Query
↓
[Node 2] Web Search
↓
[Node 3] Summarization (LLM)
↓
[Node 4] Report Generation (LLM)
↓
Final Research Report


## 🧩 Key Features

- 🔍 Automated web search
- 🧠 LLM-powered summarization
- 🧾 Structured report generation
- ⚙️ Modular node-based design
- 🔄 Extendable pipeline architecture


🧠 How It Works

This system follows a pipeline-based agent design, where each node has a specialized role:

Node	Responsibility
Parse	Cleans and interprets user input
Search	Retrieves relevant information
Summarize	Extracts key insights
Report	Produces structured output

This mirrors modern research agents that separate planning, execution, and synthesis for better reliability.

🛠️ Tech Stack
Python
OpenAI API
Requests
dotenv

