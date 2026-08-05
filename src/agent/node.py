from typing import Any, Dict

from langgraph.types import interrupt
from state import AgentState, AuditReport, BoundingBox, DiscrepancyItem


def router_controller(state: AgentState) -> Dict[str, Any]:
    """Inspects current state to decide whether tool execution or direct auditing is needed."""
    rules = state.get("regulatory_rules", [])
    crops = state.get("crop_coordinates")

    # Routing logic based on state completeness
    if not rules:
        return {"next_action": "rag_search"}
    elif crops is not None and len(crops) == 4:
        return {"next_action": "crop_roi"}
    else:
        return {"next_action": "audit"}


def tool_crop_roi(state: AgentState) -> Dict[str, Any]:
    """Pillow/OpenCV Node: Crops Region of Interest based on crop_coordinates."""
    coords = state.get("crop_coordinates")
    # Simulation of OpenCV/Pillow cropping operation
    print(f"[Tool: Crop ROI] Cropping region {coords} from {state['photo_path']}...")
    return {"crop_coordinates": None}  # Reset after processing


def tool_rag_search(state: AgentState) -> Dict[str, Any]:
    """LlamaIndex/ChromaDB Node: Retrieves ISO/OSHA regulatory clauses."""
    print(f"[Tool: RAG Search] Searching ChromaDB for compliance rules...")
    retrieved_rules = [
        "OSHA 1910.303: Minimum 36-inch clearance required in front of high-voltage breaker panels.",
        "ISO 9001: P&ID document revisions must match physical site piping layout.",
    ]
    return {"regulatory_rules": retrieved_rules}


def multimodal_auditor(state: AgentState) -> Dict[str, Any]:
    """Vision Model Node (Gemini Flash / Ollama): Cross-references schematic and photo."""
    print("[Node: Multimodal Auditor] Running visual cross-modal evaluation...")

    # Mocking Gemini 3.5 Flash output response
    mock_audit = AuditReport(
        passed=False,
        confidence_score=0.72,  # Triggers interrupt threshold (< 0.80)
        discrepancies=[
            DiscrepancyItem(
                category="OSHA Clearance Violation",
                description="Storage rack encroaching within 24 inches of high-voltage panel.",
                severity="CRITICAL",
                photo_box=BoundingBox(x1=0.15, y1=0.40, x2=0.32, y2=0.65),
            )
        ],
        regulatory_citations=["OSHA 1910.303"],
    )

    return {
        "audit_results": mock_audit.model_dump(),
        "confidence_score": mock_audit.confidence_score,
    }


def reflection_critic(state: AgentState) -> Dict[str, Any]:
    """Validates audit structure and logs confidence scoring."""
    confidence = state.get("confidence_score", 0.0)
    print(
        f"[Node: Reflection/Critic] Audit confidence score evaluated: {confidence * 100:.1f}%"
    )
    return {}


def human_in_the_loop_interrupt(state: AgentState) -> Dict[str, Any]:
    """Human-in-the-Loop Node: Uses LangGraph interrupt() to pause for manual review."""
    print(
        "[Node: Human-in-the-Loop] Confidence score below threshold (< 80%). Halting graph."
    )

    # Pauses state execution and waits for user payload
    human_decision = interrupt(
        {
            "message": "Confidence below threshold. Please review audit results.",
            "audit_results": state.get("audit_results"),
        }
    )

    return {
        "human_approved": human_decision.get("approved", False),
        "confidence_score": 1.0
        if human_decision.get("approved")
        else state["confidence_score"],
    }
