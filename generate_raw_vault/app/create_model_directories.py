from pathlib import Path


def create_directory_and_gitkeep(directory):
    path = Path(directory)
    create_model_directories(path)
    create_gitkeep_file(path)


def create_model_directories(path):
    path.mkdir(parents=True, exist_ok=True)


def create_gitkeep_file(path):
    gitkeep = path / ".gitkeep"
    gitkeep.touch(exist_ok=True)


if __name__ == "__main__":
    model_directories = [
        "source_metadata",
        "./source_tables/ddl",
        "./models/raw_vault/hubs",
        "./models/raw_vault/links",
        "./models/raw_vault/sats",
        "./models/raw_vault/stages",
    ]
    for directory in model_directories:
        create_directory_and_gitkeep(directory)
