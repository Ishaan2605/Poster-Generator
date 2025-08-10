import sys
import os
from PIL import Image, ImageFilter
import cv2
import numpy as np

# Ensure src folder is in sys.path so imports resolve correctly
src_path = os.path.abspath(os.path.dirname(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import background_removal
import poster_annotation
import template_selection
import placement
import blending


def add_noise(pil_img, amount=5):
    """Adds Gaussian noise to a PIL Image for realism."""
    arr = np.array(pil_img)
    noise = np.random.normal(0, amount, arr.shape).astype(np.int16)
    noisy = arr.astype(np.int16) + noise
    noisy_clipped = np.clip(noisy, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_clipped)


def run_pipeline(user_img_path: str, posters_dir: str, annotations_dir: str, output_dir: str):
    """
    Runs the Vogue cover replacement pipeline.

    Args:
      user_img_path (str): Path to user image.
      posters_dir (str): Directory with Vogue cover posters.
      annotations_dir (str): Directory with annotation JSON files.
      output_dir (str): Directory to save final output.

    Returns:
      str: Path to the final composited image.
    """
    poster_filename = template_selection.pick_random_poster(posters_dir)
    poster_img_path = os.path.join(posters_dir, poster_filename)
    annotation_path = os.path.join(annotations_dir, os.path.splitext(poster_filename)[0] + '.json')

    poster_img = Image.open(poster_img_path).convert("RGBA")

    annotation = poster_annotation.load_annotation(annotation_path)
    anchor = poster_annotation.get_anchor(annotation)

    os.makedirs(output_dir, exist_ok=True)
    temp_no_bg_path = os.path.join(output_dir, "temp_user_no_bg.png")

    background_removal.remove_background(user_img_path, temp_no_bg_path)
    user_img_no_bg = Image.open(temp_no_bg_path).convert("RGBA")

    user_img_no_bg = user_img_no_bg.filter(ImageFilter.GaussianBlur(radius=2))

    composited_img = placement.align_and_place(user_img_no_bg, poster_img, anchor)

    poster_cv = cv2.cvtColor(np.array(poster_img), cv2.COLOR_RGBA2BGR)
    composited_cv = cv2.cvtColor(np.array(composited_img), cv2.COLOR_RGBA2BGR)

    blended_cv = blending.reinhard_color_transfer(poster_cv, composited_cv)

    final_img = Image.fromarray(cv2.cvtColor(blended_cv, cv2.COLOR_BGR2RGBA))

    final_img = add_noise(final_img, amount=5)

    output_path = os.path.join(output_dir, f'output_{os.path.splitext(poster_filename)[0]}.png')
    final_img.save(output_path)
    print(f"Output saved to {output_path}")

    return output_path
