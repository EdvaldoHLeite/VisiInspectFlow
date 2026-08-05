from typing import Any, Dict, List, Literal, Optional, TypedDict

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """Normalized spatial coordinates [0.0 to 1.0] or pixel values for image regions."""

    x1: float = Field(..., description="Top-left X coordinate")
    y1: float = Field(..., description="Top-left Y coordinate")
    x2: float = Field(..., description="Bottom-right X coordinate")
    y2: float = Field(..., description="Bottom-right Y coordinate")
    label: Optional[str] = Field(None, description="Optional label for visual marker")


class DiscrepancyItem(BaseModel):
    """Represents a single non-compliance or drift incident detected during evaluation."""

    category: str = Field(
        ..., description="e.g., P&ID Drift, OSHA Clearance Violation, ATEX Mismatch"
    )
    description: str = Field(
        ..., description="Detailed explanation of the visual mismatch"
    )
    severity: Literal["LOW", "MEDIUM", "CRITICAL"] = Field(
        ..., description="Hazard risk level"
    )
    blueprint_box: Optional[BoundingBox] = Field(
        None, description="Bounding coordinates on CAD/blueprint"
    )
    photo_box: Optional[BoundingBox] = Field(
        None, description="Bounding coordinates on field photo"
    )


class AuditReport(BaseModel):
    """Complete structured JSON output returned by the auditor node."""

    passed: bool = Field(..., description="True if no critical discrepancies found")
    confidence_score: float = Field(
        ..., ge=0.0, le=1.0, description="Self-assessed confidence score"
    )
    discrepancies: List[DiscrepancyItem] = Field(
        default_factory=list, description="List of identified issues"
    )
    regulatory_citations: List[str] = Field(
        default_factory=list, description="Relevant OSHA/ISO clauses cited"
    )


class AgentState(TypedDict):
    """LangGraph shared execution context dictionary."""

    blueprint_path: str
    photo_path: str
    crop_coordinates: Optional[List[List[float]]]
    regulatory_rules: List[str]
    audit_results: Optional[AuditReport]
    confidence_score: float
    human_approved: Optional[bool]
    next_action: Optional[str]
