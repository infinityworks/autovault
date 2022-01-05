import pytest
from unittest.mock import patch, MagicMock, Mock
from generate_raw_vault.app.metadata_handler import Metadata
from generate_raw_vault.app.export_hub_vault_models import (
    get_hubs_from_file,
    get_unique_hubs,
    substitution_template,
    get_aggregated_hubs,
    format_aggregated_hub_sources,
)
from typing import Set, Any


@pytest.mark.usefixtures(
    "test_get_metadata_testfile_path_param", "test_get_hub_subs_string_param"
)
def test_get_hubs_from_file(
    test_get_metadata_testfile_path_param, test_get_hub_subs_string_param
):
    test_hubs_from_file = get_hubs_from_file(test_get_metadata_testfile_path_param)
    expected_hubs_from_file = test_get_hub_subs_string_param
    assert test_hubs_from_file == expected_hubs_from_file


@pytest.mark.usefixtures("test_get_hubs_from_file_param")
def test_get_unique_hubs(test_get_hubs_from_file_param):
    test_unique_hubs = get_unique_hubs(test_get_hubs_from_file_param)
    expected_unique_hubs = {"HUB1", "HUB2"}
    assert test_unique_hubs == expected_unique_hubs


@pytest.mark.usefixtures("test_hashkey_substitution_hub_param")
def test_substitution_template(test_hashkey_substitution_hub_param):
    test_substitution_template = substitution_template(
        test_hashkey_substitution_hub_param
    )
    expected_substitution_template = {
        "source_model": [],
        "hub_name": "HUB1",
        "src_pk": "HUB1_HK",
        "src_nk": "",
        "src_ldts": "LOAD_DATETIME",
        "src_source": "RECORD_SOURCE",
    }
    assert test_substitution_template == expected_substitution_template


def test_format_aggregated_hub_sources():
    aggregated_hubs: dict[str, dict[str, Any]] = {
        "hub_1": {"source_model": ["s_1", "s_2"]}
    }
    hub_name: str = "hub_1"
    formated_aggregated_hub_sources = format_aggregated_hub_sources(
        aggregated_hubs, hub_name
    )
    assert formated_aggregated_hub_sources == {
        "hub_1": {"source_model": "s_1,\n                        s_2"}
    }


@patch(
    "generate_raw_vault.app.export_hub_vault_models.substitution_template",
    return_value="test_data",
)
def test_get_aggregate_hubs(substitute_mock):
    test_data = set(["HUB1", "HUB2"])
    aggregated_hubs = get_aggregated_hubs(test_data)
    assert aggregated_hubs == {"HUB1": "test_data", "HUB2": "test_data"}
