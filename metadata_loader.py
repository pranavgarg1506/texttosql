import json

def load_metadata_from_json(file_path: str) -> dict:
    """
    Load metadata from a JSON file.
    
    :param file_path: Path to the JSON file containing metadata.
    :return: Parsed metadata as a dictionary.
    """
    with open(file_path, 'r') as f:
        metadata = json.load(f)
    return metadata