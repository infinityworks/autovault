import glob
import json
from pathlib import Path


def find_json_metadata(parent_dir):
    metadata_files = [
        Path(file) for file in glob.iglob(f"./{parent_dir}/**/*.json", recursive=True)
    ]
    return metadata_files


def load_metadata_file(metadata_path: str):
    file_path = Path(metadata_path)
    with open(file_path) as metadata_file:
        metadata = json.load(metadata_file)
    return metadata


if __name__ == "__main__":
    paths = find_json_metadata("source_metadata")
