import sys
import os

# Add src path to sys.path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import inference

def main():
    if len(sys.argv) < 4:
        print("Usage: python run_demo.py <user_image_path> <posters_dir> <annotations_dir>")
        sys.exit(1)

    user_img = sys.argv[1]
    posters_dir = sys.argv[2]
    annotations_dir = sys.argv[3]
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'outputs')

    output_path = inference.run_pipeline(user_img, posters_dir, annotations_dir, output_dir)
    print(f"Demo complete! Output at: {output_path}")

if __name__ == "__main__":
    main()
