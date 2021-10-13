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

    @pytest.mark.usefixtures("sample_metadata")
    def test_get_versioned_source_name(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_version = test_metadata.get_versioned_source_name()
        expected_target_version = "TEST_V1"
        assert test_target_version == expected_target_version

    @pytest.mark.usefixtures("sample_metadata")
    def test_get_source_business_topics(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_source_business_topics = test_metadata.get_source_business_topics()
        expected_target_source_business_topics = [
            {
                "business_keys": {"pk1": "STRING"},
                "business_attributes": [
                    {
                        "business_definition": "SAT1",
                        "payload": {"sat1_col1": "STRING", "sat1_col2": "STRING"},
                    },
                    {"business_definition": "SAT2", "payload": {"sat2_col1": "STRING"}},
                ],
            },
            {
                "business_keys": {"pk2": "STRING"},
                "business_attributes": [
                    {"business_definition": "SAT3", "payload": {"sat3_col1": "STRING"}}
                ],
            },
        ]
        assert (
            test_target_source_business_topics == expected_target_source_business_topics
        )

    @pytest.mark.usefixtures("sample_metadata")
    def test_get_hubs_from_business_topics(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_hubs = test_metadata.get_hubs_from_business_topics()
        expected_target_hubs = ["HUB1", "HUB2"]
        assert test_target_hubs == expected_target_hubs

    @pytest.mark.usefixtures("sample_metadata")
    def test_get_sats_from_source(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_sats = test_metadata.get_sats_from_source()
        expected_target_sats = {"HUB1": ["SAT1", "SAT2"], "HUB2": ["SAT3"]}
        assert test_target_sats == expected_target_sats

    @pytest.mark.usefixtures("sample_metadata")
    def test_get_sat_from_hub(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_sat = test_metadata.get_sat_from_hub("HUB1")
        expected_target_sat = ["SAT1", "SAT2"]
        assert test_target_sat == expected_target_sat

    @pytest.mark.usefixtures("sample_metadata")
    def test_get_source_attributes(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_source_attributes = test_metadata.get_source_attributes()
        expected_target_source_attributes = [
            {"sat1_col1": "STRING"},
            {"sat1_col2": "STRING"},
            {"sat2_col1": "STRING"},
            {"sat3_col1": "STRING"},
        ]
        assert test_target_source_attributes == expected_target_source_attributes

    @pytest.mark.usefixtures("sample_metadata")
    def test_flatten_business_attributes(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_flattened_attributes = test_metadata.flatten_business_attributes()
        expected_target_flattened_attributes = [
            {
                "business_definition": "SAT1",
                "payload": {"sat1_col1": "STRING", "sat1_col2": "STRING"},
            },
            {"business_definition": "SAT2", "payload": {"sat2_col1": "STRING"}},
            {"business_definition": "SAT3", "payload": {"sat3_col1": "STRING"}},
        ]
        assert test_target_flattened_attributes == expected_target_flattened_attributes
