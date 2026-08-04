# SchematicAgent

> 🚧 **Active Development:** System design and architecture specifications are finalized. Core LangGraph workflows and multimodal inspection nodes are currently being implemented.

**SchematicAgent** is a planned enterprise AI agent designed to audit engineering blueprints, CAD schematics, and floor plans against physical site photos and regulatory standards (ISO/OSHA).

It combines **LangGraph** for stateful multi-agent orchestration with **Multimodal LLMs** (Gemini 3.5 Flash-Lite / local Ollama models) and **Langfuse** for execution tracing.

---

## 🎯 Planned Features

- **Cross-Modal Verification:** Compare 2D CAD/PDF schematics with 3D physical site photos to detect equipment discrepancies and spatial violations.
- **Stateful Orchestration:** Managed graph transitions, conditional routing based on model confidence, and human-in-the-loop approval gates using **LangGraph**.
- **Structured Data Contracts:** Schema-validated JSON audit reports enforced via **Pydantic v2**.
- **Dual Inference Support:** Designed to run via cloud APIs (**Gemini 3.5 Flash-Lite**) or offline locally (**Ollama** with `llama3.2-vision`).
- **Observability:** End-to-end execution tracing and token tracking via **Langfuse**.

---

## 🏗️ Technical Architecture

For full details on data flow, state machine logic, and module breakdowns, see the complete technical specification:

- 📄 [System Architecture Document (PDF)](./SchematicAgent_Architecture_Doc.pdf)
- 📝 [Editable Design Document (Word)](./SchematicAgent_Architecture_Doc.docx)

```text
  [ Blueprint PDF / Image ] + [ Physical Field Photo ]
                          │
                          ▼
              ┌───────────────────────┐
              │  LangGraph Controller │
              └───────────┬───────────┘
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
┌─────────────────┐               ┌─────────────────┐
│ Tool: Crop ROI  │               │ Tool: RAG Search│
└────────┬────────┘               └────────┬────────┘
         │                                 │
         └────────────────┬────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  Multimodal Auditor   │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ Structured JSON Output│
              └───────────────────────┘
```

---

## 🛠️ Implementation Roadmap

- [x] System Architecture & Specification (`v1.0.0`)
- [x] Repository Structure & Environment Configuration Setup
- [ ] Pydantic Data Contracts & State Definitions (`src/models/`)
- [ ] Perception & Bounding-Box Cropping Tools (`src/tools/`)
- [ ] LangGraph State Machine & Conditional Edges (`src/agent/`)
- [ ] Gradio Interface & End-to-End Tracing Setup (`app.py`)

---

## 🧰 Stack

- **Orchestration:** LangGraph
- **Models:** Gemini 3.5 Flash-Lite / Ollama (`llama3.2-vision`)
- **Validation:** Pydantic v2
- **Vector DB / RAG:** ChromaDB / LlamaIndex
- **Observability:** Langfuse
- **Interface:** Gradio
- **Language:** Python 3.11

---

## 📄 License

Distributed under the MIT License.
