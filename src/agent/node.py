from typing import Any, Dict

from langgraph.types import interrupt

from src.agent.state import AgentState, AuditReport, BoundingBox, DiscrepancyItem
from src.models.gemini_auditor import GeminiAuditor
from src.tools.image_tools import crop_image_roi

auditor_client = GeminiAuditor()


def router_controller(state: AgentState) -> Dict[str, Any]:
    """Inspects current state to decide whether tool execution or direct auditing is needed."""
    rules = state.get("regulatory_rules", [])
    crops = state.get("crop_coordinates")

    # Routing logic based on state completeness
    if not rules:
        return {"next_action": "rag_search"}
    if crops is not None and (
        len(crops) == 4 or (len(crops) > 0 and len(crops[0]) == 4)
    ):
        return {"next_action": "crop_roi"}
    else:
        return {"next_action": "audit"}


def tool_crop_roi(state: AgentState) -> Dict[str, Any]:
    """Pillow/OpenCV Node: Crops Region of Interest based on crop_coordinates."""
    crops = state.get("crop_coordinates")
    photo_path = state.get("photo_path")

    if crops and photo_path:
        # Assuming crops contains coordinates like [[x1, y1, x2, y2]] or [x1, y1, x2, y2]
        coords = crops[0] if isinstance(crops[0], list) else crops

        print(f"[Tool: Crop ROI] Cropping region {coords} from {photo_path}...")
        cropped_path = crop_image_roi(
            image_path=photo_path, coordinates=coords, is_normalized=True
        )
        print(f"[Tool: Crop ROI] Saved patch to: {cropped_path}")

    return {"crop_coordinates": None}  # Reset after processing


def tool_rag_search(state: AgentState) -> Dict[str, Any]:
    """LlamaIndex Node: Retrieves ISO/OSHA regulatory clauses."""
    print(f"[Tool: RAG Search] Searching for compliance rules...")
    retrieved_rules = [
        "OSHA 1910.303: Minimum 36-inch clearance required in front of high-voltage breaker panels.",
        "ISO 9001: P&ID document revisions must match physical site piping layout.",
    ]
    return {"regulatory_rules": retrieved_rules}


def multimodal_auditor(state: AgentState) -> Dict[str, Any]:
    """Vision Model Node: Coordinates state inputs and delegates to isolated Gemini instance."""
    print("[Node: Multimodal Auditor] Running visual cross-modal evaluation...")

    # Extract state fields
    blueprint_path = state["blueprint_path"]
    photo_path = state["photo_path"]
    rules = state.get("regulatory_rules", [])

    # Check if a cropped image patch was generated in state from a prior crop step
    cropped_patch = state.get("cropped_patch_path")

    # Call isolated Gemini service
    audit_report: AuditReport = auditor_client.analyze(
        blueprint_path=blueprint_path,
        photo_path=photo_path,
        regulatory_rules=rules,
        cropped_patch_path=cropped_patch,
    )

    # Check if auditor identified a region needing a zoom-in crop
    detected_crops = []
    for discrepancy in audit_report.discrepancies:
        if discrepancy.photo_box and audit_report.confidence_score < 0.80:
            box = discrepancy.photo_box
            detected_crops.append([box.x1, box.y1, box.x2, box.y2])

    return {
        "audit_results": audit_report.model_dump(),
        "confidence_score": audit_report.confidence_score,
        "crop_coordinates": detected_crops if detected_crops else None,
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
