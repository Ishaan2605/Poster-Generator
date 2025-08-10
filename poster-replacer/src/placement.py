import numpy as np
import cv2
from PIL import Image

def align_and_place(user_image: Image.Image, poster_image: Image.Image, anchor: dict) -> Image.Image:
    """
    Resize user image to anchor size and alpha-blend at anchor position on poster image.
    """
    user_np = np.array(user_image)
    poster_np = np.array(poster_image.convert("RGBA"))

    # Resize user to anchor box size
    user_resized = cv2.resize(user_np, (anchor['w'], anchor['h']), interpolation=cv2.INTER_AREA)
    x, y, w, h = anchor['x'], anchor['y'], anchor['w'], anchor['h']

    # Prepare alpha mask of user image
    if user_resized.shape[2] == 3:
        user_alpha = np.ones(user_resized.shape[:2], dtype=np.uint8) * 255
    else:
        user_alpha = user_resized[:, :, 3]

    roi = poster_np[y:y+h, x:x+w]

    alpha_user = user_alpha.astype(float) / 255.0
    alpha_poster = 1.0 - alpha_user

    # Blend RGB channels
    for c in range(3):
        roi[:, :, c] = (alpha_user * user_resized[:, :, c] + alpha_poster * roi[:, :, c])
    # Set alpha channel fully opaque for composite zone
    roi[:, :, 3] = 255

    poster_np[y:y+h, x:x+w] = roi

    return Image.fromarray(poster_np)
