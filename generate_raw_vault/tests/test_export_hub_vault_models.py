import pytest
from unittest.mock import patch, MagicMock, Mock
from generate_raw_vault.app.metadata_handler import Metadata
from generate_raw_vault.app.export_hub_vault_models import (
    create_hub_substitution_template,
    format_list_ouput_with_newlines,
    get_formatted_source_name,
    get_list_of_hub_lists,
)


@pytest.mark.usefixtures("sample_metadata_class")
def test_get_formatted_source_name(sample_metadata_class):
    test_formatted_source_name = get_formatted_source_name(sample_metadata_class)
    assert test_formatted_source_name == '"stg_test_v1"'


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


def test_format_list_ouput_with_newlines():
    sources_list = ["hub_1", "hub_2"]
    formated_sources_list = format_list_ouput_with_newlines(sources_list)
    assert formated_sources_list == f"hub_1,\n{chr(32)*24}hub_2"
