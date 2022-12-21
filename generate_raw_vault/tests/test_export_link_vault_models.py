import pytest
import generate_raw_vault.app.export_link_vault_models as link_exporter
from generate_raw_vault.app.model_creation import create_substitution_values_template


@pytest.mark.usefixtures("metadata_file_dirs_fixture", "sample_metadata")
def test_get_metadata_map(metadata_file_dirs_fixture, sample_metadata):
    test_get_metadata_map = link_exporter.get_metadata_map(metadata_file_dirs_fixture)
    expected_output = {
        "generate_raw_vault/tests/fixtures/test_metadata/metadata_testfile.json": sample_metadata
    }
    assert expected_output == test_get_metadata_map


@pytest.mark.usefixtures("sample_metadata")
def test_get_map_of_source_and_hubs(sample_metadata):
    test_get_map_of_source_and_hubs = link_exporter.get_map_of_source_and_hubs(
        sample_metadata
    )
    expected_output = {"TEST_V1": ["HUB1", "HUB2"]}
    assert test_get_map_of_source_and_hubs == expected_output


@pytest.mark.usefixtures("sample_metadata_map")
def test_create_link_source_map(sample_metadata_map):
    test_create_link_source_map = link_exporter.create_link_source_map(
        sample_metadata_map
    )
    assert test_create_link_source_map == {
        "generate_raw_vault/tests/fixtures/metadata_testfile.json": "HUB1_HUB2_TEST_UoW"
    }


def test_create_link_source_map():

    link = "HUB1_HUB2_TEST_UoW"
    metadata_dict = {
        "unit_of_work": "TEST_UoW",
        "source_name": "TEST",
        "version": "1",
        "source_system": "CSV",
        "destination_database": "AUTOVAULT",
        "destination_schema": "PUBLIC",
        "business_topics": {
            "HUB1": {
                "business_keys": {"pk1": "STRING"},
                "business_attributes": [
                    {
                        "business_definition": "SAT1",
                        "payload": {"sat1_col1": "STRING", "sat1_col2": "STRING"},
                    },
                    {"business_definition": "SAT2", "payload": {"sat2_col1": "STRING"}},
                ],
            },
            "HUB2": {
                "business_keys": {"pk2": "STRING"},
                "business_attributes": [
                    {"business_definition": "SAT3", "payload": {"sat3_col1": "STRING"}}
                ],
            },
        },
    }
    substitution_values = {
        "hubs": "",
        "filename": "",
        "link_name": "",
        "source_list": [],
    }
    naming_dictionary = {
        "CUSTOMER": "CUST",
        "PRODUCT": "PRDCT",
        "TRANSACTION": "TRNSCTN",
    }
    expected_output = {
        "hubs": ["HUB1", "HUB2"],
        "filename": "hub1_hub2_test_uow",
        "link_name": "HUB1_HUB2_TEST_UoW",
        "source_list": ["TEST_V1"],
    }
    test_substitution_values = link_exporter.populate_substitution_values(
        link, metadata_dict, substitution_values, naming_dictionary
    )
    assert test_substitution_values == expected_output


def test_create_link_substitutions():
    substitution_values = {
        "hubs": ["HUB1", "HUB2"],
        "filename": "hub1_hub2_test_uow",
        "link_name": "HUB1_HUB2_TEST_UoW",
        "source_list": ["TEST_V1"],
        "source_tables": '"stg_test_v1"',
        "hash_key": "HUB1_HUB2_TEST_UOW_HK",
        "foreign_keys": f'"HUB1_HK",\n{chr(32)*18}"HUB2_HK"',
        "payload": None,
        "record_source": "RECORD_SOURCE",
        "record_load_datetime": "LOAD_DATETIME",
    }
    test_create_link_substitutions = link_exporter.create_link_substitutions(
        substitution_values
    )
    expected_output = {
        "alias": "HUB1_HUB2_TEST_UoW",
        "payload": None,
        "source_model": '"stg_test_v1"',
        "src_pk": "HUB1_HUB2_TEST_UOW_HK",
        "src_fk": '"HUB1_HK",\n                  "HUB2_HK"',
        "src_ldts": "LOAD_DATETIME",
        "src_source": "RECORD_SOURCE",
    }
    assert test_create_link_substitutions == expected_output
