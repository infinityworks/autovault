from json import load, dumps
import pytest
from pathlib import Path

METADATA_TESTFILE_PATH = Path(__file__).parent / "fixtures/metadata_testfile.json"


@pytest.fixture(scope="function")
def sample_metadata():
    test_metadata = read_file(METADATA_TESTFILE_PATH)
    return test_metadata


def read_file(path, mode="r"):
    with open(path, mode) as file:
        return load(file)
