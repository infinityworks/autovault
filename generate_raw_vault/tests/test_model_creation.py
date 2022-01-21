import pytest
from generate_raw_vault.app.model_creation import create_substitution_values_template


def test_create_substitution_values_template():
    test_template = create_substitution_values_template()
    expected_template = {
        "hubs": "",
        "filename": "",
        "link_name": "",
        "source_list": [],
        "record_load_datetime": "LOAD_DATETIME",
        "record_source": "RECORD_SOURCE",
    }
    assert test_template == expected_template
