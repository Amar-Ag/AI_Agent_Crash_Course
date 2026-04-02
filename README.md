# Data Engineering Zoomcamp AI Assistant

An AI-powered assistant that answers questions about the [DataTalksClub Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) repository using hybrid search and a Groq-powered LLM agent.

🚀 **Live Demo**: [aa10-ai-agent.streamlit.app](https://aa10-ai-agent.streamlit.app)
🎥 **Demo Video**: [Watch on Loom](https://www.loom.com/share/e0f4561cdbe74ffbba3f7cccbd12a170)

---

## Overview

Finding specific information in a large GitHub repository can be time-consuming. This assistant lets you ask natural language questions about the Data Engineering Zoomcamp course materials and get accurate, cited answers instantly.

**Example questions you can ask:**
- "How do I set up Docker for the course?"
- "What are the prerequisites for the Kafka module?"
- "How do I connect Spark to GCS?"
- "What tools do I need for module 1?"

---

## Architecture
```
GitHub Repo (DataTalksClub/data-engineering-zoomcamp)
        ↓
   ingest.py — downloads and parses 143 markdown files
        ↓
   Section-based chunking (split by ## headers → 620 sections)
        ↓
   Hybrid Search (minsearch text search + sentence-transformers vector search)
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
│   ├── data_gen.ipynb     # AI-powered question generation
│   ├── evaluations.ipynb  # LLM-as-judge evaluation pipeline
│   └── questions.json     # generated test questions
└── project.ipynb          # exploration and experimentation notebook
```

---

## Installation

**Prerequisites:** Docker + VS Code with Dev Containers extension
```bash
# Clone the repo
git clone https://github.com/Amar-Ag/AI_Agent_Crash_Course
cd AI_Agent_Crash_Course

# Open in Dev Container
# VS Code will automatically detect and prompt to reopen in container

# Navigate to the app folder
cd project/app

# Install dependencies
uv sync

# Set your Groq API key
echo "GROQ_API_KEY=your-key-here" > ../../.env
```

---

## Usage

**Streamlit UI (recommended):**
```bash
cd project/app
uv run streamlit run app.py
```

**Command line interface:**
```bash
cd project/app
uv run python main.py
```

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | Groq (`llama-3.1-8b-instant`) |
| Agent Framework | Pydantic AI |
| Text Search | minsearch |
| Vector Search | sentence-transformers (`all-MiniLM-L6-v2`) |
| UI | Streamlit |
| Deployment | Streamlit Cloud |
| Package Manager | uv |
| Dev Environment | Docker Dev Containers |

---

## Evaluation

Evaluation was conducted using **LLM-as-a-judge** methodology:

1. **Data generation** — used `llama-3.3-70b-versatile` to generate 20 realistic test questions from Zoomcamp content
2. **Agent responses** — ran each question through the Zoomcamp agent and logged all interactions
3. **Automated scoring** — used a second LLM to evaluate each response against a checklist

### Results (10 evaluated interactions)

| Check | Score |
|---|---|
| instructions_follow | 50% |
| instructions_avoid | 100% |
| answer_relevant | 50% |
| answer_clear | 40% |
| answer_citations | 50% |
| completeness | 40% |
| tool_call_search | 100% |

The agent consistently uses the search tool (100%) and avoids forbidden actions (100%). Lower scores on relevance and completeness are partly caused by tool-call format leaking with `llama-3.1-8b-instant` on specific technical questions — the raw search query appears in the response instead of being executed.

---

## Known Limitations & Future Improvements

**Current limitations:**
- `llama-3.1-8b-instant` occasionally leaks raw tool-call syntax into responses instead of executing the search — this affects answer quality for some queries
- Evaluation scores are impacted by this model behaviour on specific technical questions
- No conversation memory — the agent doesn't remember previous questions in a session

**Planned improvements:**
- Switch to a more reliable model for tool use (e.g. `llama-3.3-70b-versatile` or `gpt-4o-mini`) to eliminate tool-call leaking
- Expand the knowledge base beyond README files to include code files and homework solutions
- Add conversation memory so the agent remembers previous questions in a session
- Improve chunking strategy for highly technical sections
- Add proper CI/CD pipeline with automated tests

---

## Acknowledgments

Built as part of the [AI Agents Crash Course](https://alexeygrigorev.com/aihero/) by Alexey Grigorev at DataTalksClub.
