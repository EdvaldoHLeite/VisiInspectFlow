from typing import Any, Dict, List, Optional, TypedDict

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """Crop the industrial images for interesting zone"""

    x1: float
    y1: float
    x2: float
    y2: float
    label: Optional[str] = None


class DiscrepancyItem(BaseModel):
    """The found errors and discrepances are following this format"""

    category: str  # e.g., "Missing Component", "Clearance Violation", "P&ID Drift"
    description: str
    severity: str  # "LOW", "MEDIUM", "CRITICAL"
    blueprint_box: Optional[BoundingBox] = None
    photo_box: Optional[BoundingBox] = None


class AuditReport(BaseModel):
    """Model for the results"""

    passed: bool
    confidence_score: float = Field(ge=0.0, le=1.0)
    discrepancies: List[DiscrepancyItem] = []
    regulatory_citations: List[str] = []


class AgentState(TypedDict):
    """Graph/Controller"""

    blueprint_path: str
    photo_path: str
    crop_coordinates: Optional[List[List[float]]]
    regulatory_rules: List[str]
    audit_results: Optional[AuditReport]
    confidence_score: float
    human_approved: Optional[bool]
