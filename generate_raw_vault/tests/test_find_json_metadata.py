from generate_raw_vault.app.find_metadata_files import find_json_metadata
import pytest
from pathlib import Path


def test_find_json_metadata():
    metadata_files = find_json_metadata(
        "generate_raw_vault/tests/fixtures/test_metadata"
    )
    expected_metadata_files = [
        Path("generate_raw_vault/tests/fixtures/test_metadata/metadata_testfile.json"),
    ]
    assert metadata_files == expected_metadata_files
