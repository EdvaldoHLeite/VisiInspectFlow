from src.agent.node import tool_crop_roi
from src.agent.state import AgentState


def test_node_crop():
    """Load the sample image and crop it"""
    # Mock input state containing crop coordinates
    sample_state: AgentState = {
        "blueprint_path": "data/blueprints/sample_blueprint.png",
        "photo_path": "data/site_photos/sample_photo.jpg",
        "crop_coordinates": [[0.15, 0.40, 0.32, 0.65]],
        "regulatory_rules": [],
        "audit_results": None,
        "confidence_score": 0.0,
        "human_approved": None,
        "next_action": "crop_roi",
    }

    # Execute node
    updated_state = tool_crop_roi(sample_state)

    # Verify crop_coordinates was reset to None to prevent routing loops
    print(f"Updated state returned: {updated_state}")
    assert updated_state.get("crop_coordinates") is None, (
        "crop_coordinates failed to reset!"
    )


if __name__ == "__main__":
    test_node_crop()
