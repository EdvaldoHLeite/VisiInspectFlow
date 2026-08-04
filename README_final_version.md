> ⚠️ **Status: Active Development / System Design Stage**
> The architectural specification and documentation are finalized. Code implementation (LangGraph nodes, Gemini integrations, and evaluation routines) is currently being pushed in batches.

# SchematicAgent: Industrial Document & Diagram Auditor

An enterprise-grade, multimodal AI agent designed to audit engineering blueprints, CAD schematics (P&ID), and floor plans against physical site photos and regulatory standards (ISO/OSHA). Built with **LangGraph**, **Multimodal LLMs**, and **Langfuse Observability**, this system automates visual compliance and structural verification without traditional manual inspection loops.

---

## Key Features

- **Cross-Modal Verification:** Directly compares 2D vector/PDF blueprints against 3D physical field photographs to detect discrepancies, missing safety equipment, or spatial clearance violations.
- **Stateful Agent Workflows:** Powered by **LangGraph** to execute deterministic inspection graphs, managed state transitions, and human-in-the-loop (`interrupt()`) approval gates.
- **Strict Data Contracts:** Enforces structured JSON output via **Pydantic** schemas for pass/fail metrics, violation coordinates, and confidence scoring.
- **Dual Inference Engine:** Model-agnostic design supporting high-speed multimodal cloud inference (**Gemini 3.5 Flash-Lite** / **GPT-4o**) as well as 100% offline, privacy-focused local execution (**Ollama** with `llama3.2-vision`).
- **End-to-End Tracing:** Complete execution and tool-call observability using **Langfuse** to monitor latency, token usage, and intermediate reasoning steps.

---

## Architecture Overview

```text
  [ Blueprint (PDF/Image) ] + [ Field Site Photo ]
                          │
                          ▼
             ┌─────────────────────────┐
             │   LangGraph Router      │
             └────────────┬────────────┘
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
┌─────────────────┐               ┌─────────────────┐
│ Tool: Crop ROI  │               │ Tool: RAG Search│
│ Bounding Boxes  │               │ Regulatory Rules│
└────────┬────────┘               └────────┬────────┘
         │                                 │
         └────────────────┬────────────────┘
                          │
                          ▼
             ┌─────────────────────────┐
             │  Multimodal Auditor Node│
             │   (Visual Reasoning)    │
             └────────────┬────────────┘
                          │
                          ▼
             ┌─────────────────────────┐
             │  Structured JSON Output │
             │   (Pydantic Validation) │
             └─────────────────────────┘
```

---

## Tech Stack

| Category                    | Technology / Framework                                      |
| :-------------------------- | :---------------------------------------------------------- |
| **Agent Orchestration**     | [LangGraph](https://github.com/langchain-ai/langgraph)      |
| **Multimodal LLMs**         | Gemini 3.5 Flash-Lite / GPT-4o / Ollama (`llama3.2-vision`) |
| **Observability & Tracing** | [Langfuse](https://langfuse.com/)                           |
| **Data Validation**         | [Pydantic v2](https://docs.pydantic.dev/)                   |
| **Vector DB / RAG**         | ChromaDB / LlamaIndex                                       |
| **User Interface**          | Gradio                                                      |
| **Language & Env**          | Python 3.11                                                 |

---

## Project Structure

```text
schematic-agent/
├── data/
│   ├── blueprints/          # Sample PDF and image schematics
│   ├── site_photos/         # Field photography for validation
│   └── regulatory_docs/     # Regulatory PDFs for RAG retrieval
├── src/
│   ├── agent/
│   │   ├── graph.py         # LangGraph state machine definition
│   │   ├── nodes.py         # Inspection, execution, and critic nodes
│   │   └── state.py         # Agent state definitions
│   ├── tools/
│   │   ├── image_tools.py   # Crop ROI, image scaling, and annotation tools
│   │   └── rag_tools.py     # Regulatory document retrieval tools
│   ├── models/
│   │   └── schema.py        # Pydantic audit report models
│   └── config.py            # Environment and model settings
├── app.py                   # Gradio interface entrypoint
├── .env.example             # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Project Roadmap & Implementation Phases

This repository is transitioning from architecture design to functional code. Below is the active delivery schedule for the SchematicAgent core modules.

### Phase 1: Environment & Foundational Setup

- [ ] Initialize repository structure (`src/`, `tests/`, `config/`).
- [ ] Configure environment variables (`.env.example`) for Gemini API, ChromaDB, and Langfuse.
- [ ] Define baseline Pydantic schemas (`AgentState`, `AuditReport`, `DiscrepancyItem`).
- [ ] Set up local vector storage engine using LlamaIndex & ChromaDB.

### Phase 2: Perception & Tool Integration

- [ ] Implement OpenCV/Pillow visual pre-processing scripts (scaling, bounding-box cropping).
- [ ] Build RAG indexing tools to retrieve regulatory passages (ISO 9001 / OSHA guidelines).
- [ ] Implement Gemini 3.5 Flash-Lite multimodal visual inspection tool node.
- [ ] Construct local fallback provider bridge using Ollama (Llava / Llama 3.2 Vision).

### Phase 3: LangGraph Stateful Orchestration

- [ ] Construct core `StateGraph` definition and compile initial node connections.
- [ ] Implement conditional routing edges based on model confidence scoring.
- [ ] Integrate Human-in-the-Loop (`interrupt()`) state checkpoints for manual low-confidence overrides.
- [ ] Attach Langfuse instrumentation for full trace monitoring, latency tracking, and token usage analytics.

### Phase 4: Interface & Continuous Evaluation

- [ ] Build dynamic Gradio UI dashboard displaying side-by-side Blueprint vs. Field Photo analysis.
- [ ] Construct evaluation test suites against sample CAD/photo pairs.
- [ ] Finalize end-to-end integration tests and publish initial Release Candidate (`v1.0.0-rc`).

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- _(Optional)_ [Ollama](https://ollama.com/) installed locally for offline execution.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/schematic-agent.git
   cd schematic-agent
   ```

2. **Create and activate a virtual environment:**

   ```bash
   # Windows (PowerShell)
   python -m venv venv311
   .\venv311\Scripts\Activate.ps1

   # Linux/macOS
   python3 -m venv venv311
   source venv311/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables:**
   Copy `.env.example` to `.env` and fill in your API credentials:

   ```bash
   cp .env.example .env
   ```

   _Example `.env` configuration:_

   ```env
   # Model API Keys
   GEMINI_API_KEY="your_gemini_api_key"
   OPENAI_API_KEY="your_openai_api_key"

   # Langfuse Observability
   LANGFUSE_PUBLIC_KEY="pk-lf-..."
   LANGFUSE_SECRET_KEY="sk-lf-..."
   LANGFUSE_HOST="https://cloud.langfuse.com"

   # Agent Configuration
   DEFAULT_MODEL="gemini-3.5-flash-lite"
   USE_LOCAL_OLLAMA="false"
   ```

---

## Running the Application

### Launch the Gradio Interface

```bash
python app.py
```

Open your browser and navigate to `http://localhost:7860` to upload schematics, trigger audits, and inspect trace IDs.

### Run via Command Line

```bash
python -m src.agent.graph --blueprint data/blueprints/panel_v1.png --photo data/site_photos/photo_v1.jpg
```

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
