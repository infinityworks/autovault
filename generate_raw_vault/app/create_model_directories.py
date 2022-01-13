from pathlib import Path

model_directories = [
    "source_metadata",
    "./source_tables/DDL",
    "./models/raw_vault/hubs",
    "./models/raw_vault/links",
    "./models/raw_vault/sats",
    "./models/raw_vault/stages",
]


def create_model_directories():
    for directory in model_directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        gitkeeps = path / ".gitkeep"
        gitkeeps.touch(exist_ok=True)


if __name__ == "__main__":
    create_model_directories()
