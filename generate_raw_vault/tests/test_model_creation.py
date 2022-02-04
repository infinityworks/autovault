import pytest
from generate_raw_vault.app.model_creation import create_substitution_values_template


def test_create_substitution_values_template():
    test_template = create_substitution_values_template()
    expected_template = {
        "filename": None,
        "hash_key": None,
        "hubs": None,
        "hub_name": None,
        "link_name": None,
        "natural_key": None,
        "record_load_datetime": "LOAD_DATETIME",
        "record_source": "RECORD_SOURCE",
        "source_list": [],
    }
    assert test_template == expected_template
