import os

from PIL import Image, ImageDraw, ImageFont


def generate_mock_assets():
    """Generate samples used to test the node for cropped images"""
    os.makedirs("data/blueprints", exist_ok=True)
    os.makedirs("data/site_photos", exist_ok=True)

    blueprint_path = "data/blueprints/sample_blueprint.png"
    photo_path = "data/site_photos/sample_photo.jpg"

    # --- 1. Generate CAD Blueprint (800x600, Blue Background) ---
    bp = Image.new("RGB", (800, 600), color=(15, 32, 67))
    draw_bp = ImageDraw.Draw(bp)

    # Grid lines
    for x in range(0, 800, 50):
        draw_bp.line([(x, 0), (x, 600)], fill=(30, 60, 110), width=1)
    for y in range(0, 600, 50):
        draw_bp.line([(0, y), (800, y)], fill=(30, 60, 110), width=1)

    # Drawn component: Breaker Panel at [400, 100, 700, 300]
    draw_bp.rectangle([400, 100, 700, 300], outline=(255, 255, 255), width=3)
    draw_bp.text(
        (420, 120),
        "MAIN BREAKER PANEL\nReq. Clearance: 36 inches",
        fill=(255, 255, 255),
    )

    bp.save(blueprint_path)
    print(f"Created synthetic blueprint: {blueprint_path}")

    # --- 2. Generate Field Photo (800x600, Light Gray Background) ---
    photo = Image.new("RGB", (800, 600), color=(220, 220, 220))
    draw_photo = ImageDraw.Draw(photo)

    # Drawn component: Breaker Panel in same location [400, 100, 700, 300]
    draw_photo.rectangle(
        [400, 100, 700, 300], fill=(70, 70, 70), outline=(0, 0, 0), width=2
    )
    draw_photo.text((420, 120), "PANEL A-1", fill=(255, 255, 0))

    # Drawn Violation: Storage Crate blocking clearance [450, 220, 650, 290]
    draw_photo.rectangle(
        [450, 220, 650, 290], fill=(139, 69, 19), outline=(0, 0, 0), width=2
    )
    draw_photo.text((460, 240), "CRATE (OSHA VIOLATION)", fill=(255, 255, 255))

    photo.save(photo_path)
    print(f"Created synthetic photo: {photo_path}")

    return blueprint_path, photo_path


if __name__ == "__main__":
    generate_mock_assets()
