import os
import json

def save_to_json(content, json_filepath):
    """
    Function to save stories to a JSON file.
    """
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def load_from_json(json_filepath):
    """
    Function to load stories from a JSON file.
    """
    if os.path.exists(json_filepath):
        with open(json_filepath, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return content
    else:
        return []
