import os
import json
from typing import Dict
from PIL import Image

def create_default_anchor(image_path: str, box_fraction: float = 0.5) -> Dict:
    """
    Generates a default anchor box centered in the poster.
    - box_fraction: What fraction of the width/height the box should cover (0 < box_fraction <= 1).
    """
    with Image.open(image_path) as img:
        W, H = img.size
    w, h = int(W * box_fraction), int(H * box_fraction)
    x, y = (W - w) // 2, (H - h) // 2
    return {"x": x, "y": y, "w": w, "h": h}

def auto_generate_annotations(posters_dir: str, annotations_dir: str, anchor_type: str = "face", box_fraction: float = 0.5):
    os.makedirs(annotations_dir, exist_ok=True)
    for poster in os.listdir(posters_dir):
        if poster.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(posters_dir, poster)
            annotation = {
                "poster": poster,
                "anchor": create_default_anchor(img_path, box_fraction),
                "type": anchor_type
            }
            name = os.path.splitext(poster)[0] + ".json"
            with open(os.path.join(annotations_dir, name), "w") as f:
                json.dump(annotation, f, indent=2)
    print("Auto-generated all annotations!")

# Example usage:
if __name__ == "__main__":
    posters_dir ="../data/posters"
    annotations_dir = "../data/annotations"
    auto_generate_annotations(posters_dir, annotations_dir, anchor_type="face", box_fraction=0.5)
