from json import load, dumps
import pytest
from pathlib import Path


@pytest.fixture(scope="function")
def sample_metadata():
    test_metadata = read_file(Path(__file__).parent / "fixtures/metadata_testfile.json")
    return test_metadata


def read_file(path, mode="r"):
    with open(path, mode) as file:
        return load(file)
