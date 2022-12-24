import pytest
from generate_raw_vault.app.export_ddl_statement import format_column_and_dtype


@pytest.mark.usefixtures("format_column_and_dtype_param")
def test_format_column_and_dtype(format_column_and_dtype_param):
    test_target_format = format_column_and_dtype(format_column_and_dtype_param)
    expected_target_format = f'"CUSTOMER_ID" STRING,\n{4*chr(32)}"PRODUCT_ID" STRING'
    assert test_target_format == expected_target_format
