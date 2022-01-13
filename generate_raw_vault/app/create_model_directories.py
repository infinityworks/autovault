from pathlib import Path


def create_model_directories(model_directories):
    for directory in model_directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        gitkeep = path / ".gitkeep"
        gitkeep.touch(exist_ok=True)


if __name__ == "__main__":
    model_directories = [
        "source_metadata",
        "./source_tables/DDL",
        "./models/raw_vault/hubs",
        "./models/raw_vault/links",
        "./models/raw_vault/sats",
        "./models/raw_vault/stages",
    ]
    create_model_directories(model_directories)
