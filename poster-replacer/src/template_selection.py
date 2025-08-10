import os
import random

def pick_random_poster(posters_dir: str) -> str:
    posters = [f for f in os.listdir(posters_dir) if f.lower().endswith(('.jpg','.png','.jpeg'))]
    if not posters:
        raise ValueError("No poster images found in directory!")
    return random.choice(posters)
