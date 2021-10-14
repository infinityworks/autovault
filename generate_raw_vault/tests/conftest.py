from json import load, dumps
import pytest
from pathlib import Path

METADATA_TESTFILE_PATH = Path(__file__).parent / "fixtures/metadata_testfile.json"


@pytest.fixture(scope="function")
def sample_metadata():
    test_metadata = read_file(METADATA_TESTFILE_PATH)
    return test_metadata


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
