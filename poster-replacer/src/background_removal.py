import os
from rembg import remove
from PIL import Image
import io

def remove_background(input_image_path: str, output_image_path: str):
    """
    Removes the background from the input image and saves the output image.
    
    Parameters:
    - input_image_path: path to the input image file (e.g., '../data/user_inputs/photo.jpg')
    - output_image_path: path where the output image with transparent background will be saved
      (e.g., '../data/outputs/photo_no_bg.png')
    """
    # Read input image bytes
    with open(input_image_path, 'rb') as input_file:
        input_bytes = input_file.read()
    
    # Remove background using rembg (U2-Net model internally)
    output_bytes = remove(input_bytes)
    
    # Convert result bytes to a PIL Image with RGBA (alpha) channel
    output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_image_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Save output image
    output_image.save(output_image_path)
    print(f"Background removed image saved to: {output_image_path}")


if __name__ == "__main__":
    # Example usage - adjust paths to your files as needed
    input_path = r"../data/user_inputs/123.jpg"
    output_path = r"../data/outputs/sample_photo_no_bg.png"
    remove_background(input_path, output_path)
