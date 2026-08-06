import os

from PIL import Image

from src.tools.image_tools import crop_image_roi

# run with: python -m tests.test_crop


def create_test_image(filename: str = "test_field_photo.jpg"):
    """Creates a simple 800x600 test image with colored quadrants."""
    img = Image.new("RGB", (800, 600), color=(255, 255, 255))
    # Draw a colored region in the top-right quadrant [0.5, 0.0, 1.0, 0.5]
    for x in range(400, 800):
        for y in range(0, 300):
            img.putpixel((x, y), (255, 150, 0))  # Red block
    img.save(filename)
    return filename


def test_crop_pipeline():
    """Loading the image and cropping it"""
    # 1. Setup sample image
    test_img_path = create_test_image()
    print(f"Created test image: {test_img_path} (800x600)")

    # 2. Test relative normalized coordinates [x1, y1, x2, y2]
    # Target top-right red quadrant (50% to 100% X, 0% to 50% Y)
    normalized_coords = [0.35, 0.15, 0.85, 0.65]

    output_crop_path = crop_image_roi(
        image_path=test_img_path,
        coordinates=normalized_coords,
        output_path="test_crop_output.jpg",
        is_normalized=True,
    )

    # 3. Assertions
    assert os.path.exists(output_crop_path), "Cropped file was not created!"

    with Image.open(output_crop_path) as cropped:
        width, height = cropped.size
        print(
            f"Successfully cropped ROI! Output path: {output_crop_path}, Dimensions: {width}x{height}"
        )
        assert width == 400 and height == 300, f"Expected 400x300, got {width}x{height}"

    # Clean up test artifacts
    os.remove(test_img_path)
    os.remove(output_crop_path)
    print("Verification passed! All test files cleaned up.")


if __name__ == "__main__":
    # create_test_image()
    test_crop_pipeline()
