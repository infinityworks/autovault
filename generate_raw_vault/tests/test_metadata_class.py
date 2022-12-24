from generate_raw_vault.app.metadata_handler import Metadata
import pytest


class TestMetadata:
    @pytest.mark.usefixtures("sample_metadata")
    def test_get_unit_of_work(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_UOW = test_metadata.get_unit_of_work()
        expected_target_UOW = "TEST_UoW"
        assert test_target_UOW == expected_target_UOW

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
                "business_keys": {"pk1": {"alias": "pk1", "type": "STRING"}},
                "business_attributes": [
                    {
                        "business_definition": "SAT1",
                        "payload": {"sat1_col1": "STRING", "sat1_col2": "STRING"},
                    },
                    {"business_definition": "SAT2", "payload": {"sat2_col1": "STRING"}},
                ],
            },
            {
                "business_keys": {"pk2": {"type": "STRING"}},
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
    def test_get_sat_from_hub(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_sat = test_metadata.get_sat_from_hub("HUB1")
        print(test_target_sat)
        expected_target_sat = {
            "SAT1": {"sat1_col1": "STRING", "sat1_col2": "STRING"},
            "SAT2": {"sat2_col1": "STRING"},
        }
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

    @pytest.mark.usefixtures("sample_metadata", "get_attrs_param")
    def test_get_attributes(self, sample_metadata, get_attrs_param):
        test_metadata = Metadata(sample_metadata)
        test_target_attribute = test_metadata.get_attributes(get_attrs_param)
        expected_target_attribute = [{"sat1_col1": "STRING"}, {"sat1_col2": "STRING"}]
        assert test_target_attribute == expected_target_attribute

    @pytest.mark.usefixtures("sample_metadata")
    def test_get_business_keys(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_business_keys = test_metadata.get_business_keys()
        expected_target_business_keys = {
            "HUB1": {"business_keys": {"pk1": {"alias": "pk1", "type": "STRING"}}},
            "HUB2": {"business_keys": {"pk2": {"type": "STRING"}}},
        }
        assert test_target_business_keys == expected_target_business_keys

    @pytest.mark.usefixtures("sample_metadata")
    def test_get_business_topics(self, sample_metadata):
        test_metadata = Metadata(sample_metadata)
        test_target_business_topics = test_metadata.get_business_topics()
        expected_target_business_topics = {
            "HUB1": {
                "business_keys": {"pk1": {"alias": "pk1", "type": "STRING"}},
                "business_attributes": [
                    {
                        "business_definition": "SAT1",
                        "payload": {"sat1_col1": "STRING", "sat1_col2": "STRING"},
                    },
                    {"business_definition": "SAT2", "payload": {"sat2_col1": "STRING"}},
                ],
            },
            "HUB2": {
                "business_keys": {"pk2": {"type": "STRING"}},
                "business_attributes": [
                    {"business_definition": "SAT3", "payload": {"sat3_col1": "STRING"}}
                ],
            },
        }
        assert test_target_business_topics == expected_target_business_topics
