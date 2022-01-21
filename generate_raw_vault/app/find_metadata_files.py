import glob
import json
from pathlib import Path
from string import Template


def find_json_metadata(metadata_directory):
    metadata_files = [
        Path(file)
        for file in glob.iglob(f"./{metadata_directory}/**/*.json", recursive=True)
    ]
    return metadata_files


def load_metadata_file(metadata_path: str):
    file_path = Path(metadata_path)
    with open(file_path) as metadata_file:
        metadata = json.load(metadata_file)
    return metadata


def load_template(template):
    template_file = load_template_file(template)
    template = Template(template_file)
    return template


def load_template_file(template_path: str):
    file_path = Path(template_path)
    with open(file_path) as template_file:
        template = template_file.read()
    return template


if __name__ == "__main__":
    paths = find_json_metadata("source_metadata")
