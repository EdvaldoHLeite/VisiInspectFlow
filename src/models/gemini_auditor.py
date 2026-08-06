import os
from typing import List, Optional

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from PIL import Image

from src.agent.state import AuditReport, BoundingBox

load_dotenv()


class GeminiAuditor:
    def __init__(self, model_name: str = "gemini-3.1-flash-lite"):
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.1,
            # api_key=os.getenv("GEMINI_API_KEY"),
        ).with_structured_output(AuditReport)

    def analyze(
        self,
        blueprint_path: str,
        photo_path: str,
        regulatory_rules: List[str],
        cropped_patch_path: Optional[str] = None,
    ) -> AuditReport:
        # Load visual inputs
        blueprint_img = Image.open(blueprint_path)
        photo_img = Image.open(photo_path)

        images = [blueprint_img, photo_img]
        if cropped_patch_path and os.path.exists(cropped_patch_path):
            images.append(Image.open(cropped_patch_path))

        # System Prompt instructing spatial analysis and coordinate extraction
        prompt = f"""
        You are an industrial compliance inspector. Cross-reference the CAD blueprint image with the field photo.
        
        Applicable Regulatory Rules:
        {chr(10).join(f"- {rule}" for rule in regulatory_rules)}

        Perform visual inspection:
        1. Identify non-compliance, missing equipment, or safety violations.
        2. Assign a confidence score [0.0 to 1.0].
        3. If suspicious regions require a closer inspection crop, include normalized bounding coordinates in photo_box [x1, y1, x2, y2].
        """

        # Multimodal invocation
        response = self.llm.invoke([prompt, *images])
        return response
