from generate_raw_vault.app.load_metadata import load_metadata_file
from json import loads
import pytest


@pytest.mark.usefixtures("sample_metadata")
def test_load_metadata_file(sample_metadata):
    test_json = """{
    "business_topics": {
        "HUB1": {
            "business_attributes": [{
                "business_definition": "SAT1",
                "payload": {
                    "sat1_col1": "STRING",
                    "sat1_col2": "STRING"
                }
            }, {
                "business_definition": "SAT2",
                "payload": {
                    "sat2_col1": "STRING"
                }
            }],
            "business_keys": {
                "pk1": "STRING"
            }
        },
        "HUB2": {
            "business_attributes": [{
                "business_definition": "SAT3",
                "payload": {
                    "sat3_col1": "STRING"
                }
            }],
            "business_keys": {
                "pk2": "STRING"
            }
        }
    },
    "destination_database": "AUTOVAULT",
    "destination_schema": "PUBLIC",
    "source_name": "TEST",
    "source_system": "CSV",
    "version": "1"
    }"""
    assert sample_metadata == loads(test_json)
