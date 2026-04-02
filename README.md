# Data Engineering Zoomcamp AI Assistant

An AI-powered assistant that answers questions about the [DataTalksClub Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) repository using hybrid search and a Groq-powered LLM agent.

🚀 **Live Demo**: [aa10-ai-agent.streamlit.app](https://aa10-ai-agent.streamlit.app)

---

## Overview

Finding specific information in a large GitHub repository can be time-consuming. This assistant lets you ask natural language questions about the Data Engineering Zoomcamp course materials and get accurate, cited answers instantly.

**Example questions you can ask:**
- "How do I set up Docker for the course?"
- "What are the prerequisites for the Kafka module?"
- "How do I connect Spark to GCS?"

---

## Architecture
```
GitHub Repo (DataTalksClub/data-engineering-zoomcamp)
        ↓
   ingest.py — downloads and parses markdown files
        ↓
   Section-based chunking (split by ## headers)
        ↓
   Hybrid Search (minsearch + sentence-transformers)
        ↓
   Pydantic AI Agent (Groq llama-3.1-8b-instant)
        ↓
   Streamlit UI (deployed on Streamlit Cloud)
```

---

## Project Structure
```
project/
├── app/
│   ├── ingest.py          # data ingestion and indexing
│   ├── search_tools.py    # hybrid search implementation
│   ├── search_agent.py    # Pydantic AI agent setup
│   ├── logs.py            # interaction logging
│   ├── app.py             # Streamlit UI
│   └── main.py            # CLI interface
├── eval/
│   ├── data_gen.ipynb     # AI question generation
│   ├── evaluations.ipynb  # LLM-as-judge evaluation
│   └── questions.json     # generated test questions
└── project.ipynb          # exploration notebook
```

---

## Installation

**Prerequisites:** Docker + VS Code with Dev Containers extension
```bash
# Clone the repo
git clone https://github.com/Amar-Ag/AI_Agent_Crash_Course
cd AI_Agent_Crash_Course

# Open in Dev Container (VS Code will prompt automatically)
# Then navigate to the app folder
cd project/app

# Install dependencies
uv sync

# Set your Groq API key
echo "GROQ_API_KEY=your-key-here" > ../../.env
```

---

## Usage

**Streamlit UI:**
```bash
cd project/app
uv run streamlit run app.py
```

**Command line:**
```bash
cd project/app
uv run python main.py
```

---

## Evaluation

Evaluation was conducted using **LLM-as-a-judge** on 10 AI-generated questions.

| Check | Score |
|---|---|
| instructions_follow | 50% |
| instructions_avoid | 100% |
| answer_relevant | 50% |
| answer_clear | 40% |
| answer_citations | 50% |
| completeness | 40% |
| tool_call_search | 100% |

The agent consistently uses the search tool and avoids forbidden actions. Lower scores on relevance and completeness are partly due to occasional tool-call format issues with the Groq `llama-3.1-8b-instant` model on highly specific technical questions. Improving chunking strategy and switching to a more reliable model would likely improve these scores.

---

## Tech Stack

- **LLM**: Groq (`llama-3.1-8b-instant`)
- **Agent Framework**: Pydantic AI
- **Search**: minsearch (text) + sentence-transformers (vector) = hybrid search
- **UI**: Streamlit
- **Deployment**: Streamlit Cloud
- **Package Manager**: uv

---

## Acknowledgments

Built as part of the [AI Agents Crash Course](https://alexeygrigorev.com/aihero/) by Alexey Grigorev.
