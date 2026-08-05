from langgraph.graph import END
from state import AgentState


def route_tools(state: AgentState) -> str:
    """Routes execution from router_controller to designated tool or auditor."""
    action = state.get("next_action")
    if action == "rag_search":
        return "tool_rag_search"
    elif action == "crop_roi":
        return "tool_crop_roi"
    return "multimodal_auditor"


def route_confidence_check(state: AgentState) -> str:
    """Evaluates whether to invoke human-in-the-loop interrupt or complete execution."""
    confidence = state.get("confidence_score", 0.0)
    if confidence < 0.80:
        return "human_in_the_loop_interrupt"
    return END
