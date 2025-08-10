import json
from typing import Dict

def load_annotation(json_path: str) -> Dict:
    """Load a poster annotation from a JSON file."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def get_anchor(annotation: Dict) -> Dict:
    """Get the anchor box details from the annotation."""
    return annotation.get('anchor', {})

def get_anchor_type(annotation: Dict) -> str:
    """Get the anchor type (e.g., 'face') from the annotation."""
    return annotation.get('type', 'face')
