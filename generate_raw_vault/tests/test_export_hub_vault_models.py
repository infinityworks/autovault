import pytest
from unittest.mock import patch, MagicMock, Mock
from generate_raw_vault.app import metadata_handler
from generate_raw_vault.app.metadata_handler import Metadata
from generate_raw_vault.app.export_hub_vault_models import (
    create_hub_substitution_template,
    format_hub_name,
    format_sources_list,
    format_source_name,
    get_unique_hubs,
    get_list_of_hub_lists,
)
from typing import Set, Any


# @pytest.mark.usefixtures(
#     "test_get_metadata_testfile_path_param", "test_get_hub_subs_string_param"
# )
# def test_get_hubs_from_file(
#     test_get_metadata_testfile_path_param, test_get_hub_subs_string_param
# ):
#     test_hubs_from_file = get_hubs_from_file(test_get_metadata_testfile_path_param)
#     expected_hubs_from_file = test_get_hub_subs_string_param
#     assert test_hubs_from_file == expected_hubs_from_file


@pytest.mark.usefixtures("test_get_hubs_from_file_param")
def test_get_unique_hubs(test_get_hubs_from_file_param):
    test_unique_hubs = get_unique_hubs(test_get_hubs_from_file_param)
    expected_unique_hubs = ["HUB1", "HUB2"]
    assert test_unique_hubs == expected_unique_hubs


def test_format_hub_name():
    test_format_hub_name = format_hub_name("HUB1")
    assert test_format_hub_name == "hub1_hub"


@pytest.mark.usefixtures("sample_metadata_class")
def test_format_source_name(sample_metadata_class):
    test_format_source_name = format_source_name(sample_metadata_class)
    assert test_format_source_name == '"stg_test_v1"'


@patch(
    "generate_raw_vault.app.metadata_handler.Metadata.get_hubs_from_business_topics",
)
def test_get_list_of_hub_lists(substitute_mock):
    substitute_mock.values = Mock(
        return_value=[
            Mock(
                spec=Metadata,
                get_hubs_from_business_topics=MagicMock(return_value=["HUB1"]),
            ),
            Mock(
                spec=Metadata,
                get_hubs_from_business_topics=MagicMock(return_value=["HUB2", "HUB3"]),
            ),
        ]
    )

    test_hub_lists = get_list_of_hub_lists(substitute_mock)
    assert test_hub_lists == [["HUB1"], ["HUB2", "HUB3"]]


@pytest.mark.usefixtures("test_substitution_values")
def test_create_hub_substitution_template(test_substitution_values):
    test_create_link_substitution = create_hub_substitution_template(
        test_substitution_values
    )
    expected_create_link_substitution = {
        "source_list": [],
        "hub_name": None,
        "src_pk": None,
        "src_nk": None,
        "src_ldts": "LOAD_DATETIME",
        "src_source": "RECORD_SOURCE",
    }
    assert test_create_link_substitution == expected_create_link_substitution


def test_format_sources_list():
    sources_list = ["hub_1", "hub_2"]
    formated_sources_list = format_sources_list(sources_list)
    assert formated_sources_list == f"hub_1,\n{chr(32)*24}hub_2"
