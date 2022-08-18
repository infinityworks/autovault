import pytest
import textwrap
from generate_raw_vault.tests.conftest import (
    hub_alias_subs_string_topics_with_alias_param,
    hub_alias_subs_string_topics,
)
from unittest.mock import MagicMock
from generate_raw_vault.app.metadata_handler import Metadata
from generate_raw_vault.app.export_staging_vault_models import (
    get_sat_substitutions_string,
    hashkey_substitution,
    get_sat_subs,
    get_sat_substitution_from_topic,
    get_hub_substitutions_string,
    get_unique_link_combinations_substitutions_string,
    get_hub_alias_substitutions_string,
    get_sat_substitutions_string,
)


@pytest.mark.usefixtures("sample_metadata", "test_hashkey_substitution_hub_param")
def test_hashkey_substitution(sample_metadata, test_hashkey_substitution_hub_param):
    test_hashkey_substitution = hashkey_substitution(
        Metadata(sample_metadata), test_hashkey_substitution_hub_param
    )
    expected_hashkey_substitution = '  HUB1_HK:\n    - "pk1"'
    assert test_hashkey_substitution == expected_hashkey_substitution


@pytest.mark.usefixtures(
    "test_get_sat_subs_sat_name_param", "test_get_sat_subs_payload_param"
)
def test_get_sat_subs(
    test_get_sat_subs_sat_name_param, test_get_sat_subs_payload_param
):
    mock_template = MagicMock()
    expected_sat_subs = {
        "hashdiff_name": "SAT1_HASHDIFF",
        "columns": '- "sat1_col1"\n      - "sat1_col2"',
    }
    get_sat_subs(
        mock_template, test_get_sat_subs_sat_name_param, test_get_sat_subs_payload_param
    )
    mock_template.substitute.assert_called_with(expected_sat_subs)


@pytest.mark.usefixtures("sample_metadata", "test_hashkey_substitution_hub_param")
def test_get_sat_substitution_from_topic(
    sample_metadata, test_hashkey_substitution_hub_param
):
    sat_substitution_from_topic = get_sat_substitution_from_topic(
        Metadata(sample_metadata), test_hashkey_substitution_hub_param
    )
    expected_sat_substitution_from_topic = textwrap.indent(
        textwrap.dedent(
            """  SAT1_HASHDIFF:
    is_hashdiff: true
    columns:
      - "sat1_col1"
      - "sat1_col2"

  SAT2_HASHDIFF:
    is_hashdiff: true
    columns:
      - "sat2_col1"
    """
        ),
        "  ",
    )
    assert sat_substitution_from_topic == expected_sat_substitution_from_topic


def test_get_hub_substitutions_string(sample_metadata, test_get_hub_subs_string_param):
    test_hub_substitutions_string = get_hub_substitutions_string(
        Metadata(sample_metadata), test_get_hub_subs_string_param
    )
    expected_hub_substitutions_string = (
        '  HUB1_HK:\n    - "pk1"\n  HUB2_HK:\n    - "pk2"'
    )
    assert test_hub_substitutions_string == expected_hub_substitutions_string


@pytest.mark.usefixtures(
    "sample_metadata",
    "test_get_hub_subs_string_param",
    "test_naming_dictionary_path",
)
def test_get_unique_link_combinations_substitutions_string(
    sample_metadata,
    test_get_hub_subs_string_param,
    test_naming_dictionary_path,
):
    test_link_substitutions_string = get_unique_link_combinations_substitutions_string(
        Metadata(sample_metadata),
        test_get_hub_subs_string_param,
        test_naming_dictionary_path,
    )
    expected_link_substitutions_string = (
        '  H1_H2_TEST_UoW_HK:\n    - "pk1"\n    - "pk2"'
    )
    assert test_link_substitutions_string == expected_link_substitutions_string


@pytest.mark.usefixtures("sample_metadata_class")
def test_get_hub_alias_substitutions_string(sample_metadata_class):
    test_hub_alias_substitutions_string = get_hub_alias_substitutions_string(
        sample_metadata_class
    )
    expected_hub_alias_substitutions_string = ""
    assert (
        test_hub_alias_substitutions_string == expected_hub_alias_substitutions_string
    )


@pytest.mark.usefixtures("sample_metadata", "test_get_sat_subs_string_topics_param")
def test_get_sat_substitution_string(
    sample_metadata, test_get_sat_subs_string_topics_param
):
    test_sat_substitution_string = get_sat_substitutions_string(
        Metadata(sample_metadata), test_get_sat_subs_string_topics_param
    )
    expected_sat_substitution_string = textwrap.indent(
        textwrap.dedent(
            """SAT1_HASHDIFF:
  is_hashdiff: true
  columns:
    - "sat1_col1"
    - "sat1_col2"

SAT2_HASHDIFF:
  is_hashdiff: true
  columns:
    - "sat2_col1"

SAT3_HASHDIFF:
  is_hashdiff: true
  columns:
    - "sat3_col1"
    """
        ),
        "  ",
    )
    assert test_sat_substitution_string == expected_sat_substitution_string
