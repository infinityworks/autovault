from json import load, dumps
from generate_raw_vault.app.metadata_handler import Metadata
import pytest
from pathlib import Path
from generate_raw_vault.app.metadata_handler import Metadata

METADATA_TESTFILE_PATH = Path(__file__).parent / "fixtures/metadata_testfile.json"
SAT_HASHDIFF_TESTTEMPLATE = "generate_raw_vault/app/templates/sat_hashdiff.sql"
NAME_DICTIONARY = "generate_raw_vault/name_dictionary.json"


@pytest.fixture(scope="function")
def sample_metadata():
    test_metadata = read_file(METADATA_TESTFILE_PATH)
    return test_metadata


@pytest.fixture(scope="function")
def sample_metadata_class():
    return Metadata(sample_metadata())


def read_file(path, mode="r"):
    with open(path, mode) as file:
        return load(file)


@pytest.fixture(scope="function")
def get_attrs_param():
    return {
        "business_definition": "SAT1",
        "payload": {"sat1_col1": "STRING", "sat1_col2": "STRING"},
    }


@pytest.fixture(scope="function")
def format_column_and_dtype_param():
    return [{"CUSTOMER_ID": "STRING"}, {"PRODUCT_ID": "STRING"}]


@pytest.fixture(scope="function")
def create_ddl_statement_params():
    params_list = [
        '"CUSTOMER_ID" STRING,\n    "PRODUCT_ID" STRING',
        '"AVG_MONTHLY_VISITS" STRING,\n    "sat1_col3" STRING,\n    "sat2_col2" STRING,\n    "sat3_col2" STRING',
        "AUTOVAULT",
        "PUBLIC",
        "CUSTOMERS_V1",
    ]
    return params_list


@pytest.fixture(scope="function")
def create_ddl_statement_targetddl():
    return """CREATE TABLE "AUTOVAULT"."PUBLIC"."CUSTOMERS_V1" (
    "CUSTOMER_ID" STRING,
    "PRODUCT_ID" STRING,
    "AVG_MONTHLY_VISITS" STRING,
    "sat1_col3" STRING,
    "sat2_col2" STRING,
    "sat3_col2" STRING,
    "RECORD_SOURCE" STRING,
    "LOAD_DATETIME" TIMESTAMP_TZ
    );
    """


@pytest.fixture(scope="function")
def test_hashkey_substitution_hub_param():
    return "HUB1"


@pytest.fixture(scope="function")
def sample_metadata_class():
    test_metadata_class = Metadata(sample_metadata())
    return test_metadata_class


@pytest.fixture(scope="function")
def hubs_substitutions():
    return ['HUB1_HK: "pk1"', 'HUB2_HK: "pk2"']


@pytest.fixture(scope="function")
def test_get_sat_subs_sat_name_param():
    return "SAT1"


@pytest.fixture(scope="function")
def test_get_sat_subs_payload_param():
    return {"sat1_col1": "STRING", "sat1_col2": "STRING"}


@pytest.fixture(scope="function")
def test_get_hub_subs_string_param():
    return ["HUB1", "HUB2"]


@pytest.fixture(scope="function")
def test_get_hubs_from_file_param():
    return [["HUB1", "HUB2"]]


@pytest.fixture(scope="function")
def test_get_unique_link_combi_string_dict_param():
    return "./test_name_dictionary.json"


@pytest.fixture(scope="function")
def test_get_metadata_testfile_path_param():
    return METADATA_TESTFILE_PATH


hub_alias_subs_string_topics = {
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
}


@pytest.fixture(scope="function")
def test_get_hub_alias_subs_string_topics_param():
    return hub_alias_subs_string_topics


hub_alias_subs_string_topics_with_alias_param = {
    "HUB1": {
        "business_keys": {"pk1": "STRING"},
        "alias": "HB1",
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
        "alias": "HB2",
        "business_attributes": [
            {"business_definition": "SAT3", "payload": {"sat3_col1": "STRING"}}
        ],
    },
}


@pytest.fixture(scope="function")
def test_get_hub_alias_subs_string_topics_with_alias_param():
    return hub_alias_subs_string_topics_with_alias_param


@pytest.fixture(scope="function")
def test_get_sat_subs_string_topics_param():
    return {
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
    }


@pytest.fixture(scope="function")
def test_get_business_topics_param():
    return {
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
    }


def metadata_file_dirs_fixture():
    return [Path("generate_raw_vault/tests/fixtures/metadata_testfile.json")]


@pytest.fixture(scope="function")
def sample_metadata_map():
    test_metadata = read_file(METADATA_TESTFILE_PATH)
    sample_metadata_map = {
        "generate_raw_vault/tests/fixtures/metadata_testfile.json": test_metadata
    }
    return sample_metadata_map
