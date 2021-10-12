from generate_raw_vault.app.load_metadata import Metadata
import pytest


class TestMetadata:
    @pytest.mark.usefixtures("sample_metadata")
    def test_get_target_schema(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_schema = test_metadata.get_target_schema()
        expected_target_schema = "PUBLIC"
        assert test_target_schema == expected_target_schema

    @pytest.mark.usefixtures("sample_metadata")
    def test_get_target_database(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_database = test_metadata.get_target_database()
        expected_target_database = "AUTOVAULT"
        assert test_target_database == expected_target_database
