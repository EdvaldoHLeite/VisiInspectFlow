from edge import route_confidence_check, route_tools
from langgraph.graph import END, START, StateGraph
from node import (
    human_in_the_loop_interrupt,
    multimodal_auditor,
    reflection_critic,
    router_controller,
    tool_crop_roi,
    tool_rag_search,
)
from state import AgentState


def build_visio_inspect_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("router_controller", router_controller)
    workflow.add_node("tool_crop_roi", tool_crop_roi)
    # workflow.add_node("tool_rag_search", tool_rag_search)
    # workflow.add_node("multimodal_auditor", multimodal_auditor)
    # workflow.add_node("reflection_critic", reflection_critic)
    # workflow.add_node("human_in_the_loop_interrupt", human_in_the_loop_interrupt)

    # Add Edges
    workflow.add_edge(START, "router_controller")

    # Conditional routing from router
    workflow.add_conditional_edges(
        "router_controller",
        route_tools,
        {
            "tool_rag_search": "tool_rag_search",
            "tool_crop_roi": "tool_crop_roi",
            "multimodal_auditor": "multimodal_auditor",
        },
    )

    # Tool returns back to multimodal auditor
    workflow.add_edge("tool_rag_search", "multimodal_auditor")
    workflow.add_edge("tool_crop_roi", "multimodal_auditor")

    # Auditor -> Critic
    workflow.add_edge("multimodal_auditor", "reflection_critic")

    # Conditional routing from reflection critic based on confidence (< 0.80)
    workflow.add_conditional_edges(
        "reflection_critic",
        route_confidence_check,
        {"human_in_the_loop_interrupt": "human_in_the_loop_interrupt", END: END},
    )

    # Human-in-the-Loop resolves directly to END
    workflow.add_edge("human_in_the_loop_interrupt", END)

    return workflow.compile()


# Instantiated StateGraph instance
visio_inspect_app = build_visio_inspect_graph()
