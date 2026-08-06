import os
from typing import List, Optional, Tuple, Union

import cv2
from PIL import Image


def crop_image_roi(
    image_path: str,
    coordinates: List[float],
    output_path: Optional[str] = None,
    is_normalized: bool = True,
) -> str:
    """Crops a Region of Interest (ROI) from an image given bounding box coordinates [x1, y1, x2, y2].

    Args:
        image_path: Filepath to the target image (blueprint or photo).
        coordinates: Bounding box list [x1, y1, x2, y2].
        output_path: Optional path to save cropped image. Generates default if None.
        is_normalized: True if coordinates are floats in range [0.0, 1.0].

    Returns:
        str: Filepath to the saved cropped image patch.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Source image not found at: {image_path}")

    if len(coordinates) != 4:
        raise ValueError(
            f"Coordinates must contain 4 values [x1, y1, x2, y2], got {coordinates}"
        )

    with Image.open(image_path) as img:
        width, height = img.size
        x1, y1, x2, y2 = coordinates

        # Denormalize relative coordinates to absolute pixel bounds if required
        if is_normalized:
            x1 = int(x1 * width)
            y1 = int(y1 * height)
            x2 = int(x2 * width)
            y2 = int(y2 * height)
        else:
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Ensure valid bounding boundaries
        x1, x2 = max(0, min(x1, width)), max(0, min(x2, width))
        y1, y2 = max(0, min(y1, height)), max(0, min(y2, height))

        cropped_img = img.crop((x1, y1, x2, y2))

        if output_path is None:
            base, ext = os.path.splitext(image_path)
            output_path = f"{base}_cropped_roi{ext}"

        cropped_img.save(output_path)
        return output_path


def annotate_bounding_boxes(
    image_path: str,
    boxes: List[Tuple[float, float, float, float]],
    labels: Optional[List[str]] = None,
    output_path: Optional[str] = None,
    is_normalized: bool = True,
) -> str:
    """Draws visual bounding boxes over an image for UI inspection using OpenCV.

    Args:
        image_path: Filepath to original image.
        boxes: List of tuples/lists with [x1, y1, x2, y2] coordinates.
        labels: Optional label strings corresponding to each box.
        output_path: Optional output path.
        is_normalized: True if coordinates are in [0.0, 1.0] relative scale.

    Returns:
        str: Filepath to the annotated image.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"OpenCV could not load image at: {image_path}")

    height, width, _ = image.shape

    for idx, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        if is_normalized:
            x1, y1, x2, y2 = (
                int(x1 * width),
                int(y1 * height),
                int(x2 * width),
                int(y2 * height),
            )
        else:
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Red bounding box (BGR format)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        if labels and idx < len(labels):
            label = labels[idx]
            cv2.putText(
                image,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_annotated{ext}"

    cv2.imwrite(output_path, image)
    return output_path
