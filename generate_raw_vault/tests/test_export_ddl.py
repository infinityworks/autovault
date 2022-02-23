import pytest
from generate_raw_vault.app.export_ddl_statement import format_column_and_dtype
from generate_raw_vault.app.export_ddl_statement import (
    create_ddl_without_transaction_payload_statement,
)


@pytest.mark.usefixtures("format_column_and_dtype_param")
def test_format_column_and_dtype(format_column_and_dtype_param):
    test_target_format = format_column_and_dtype(format_column_and_dtype_param)
    expected_target_format = f'"CUSTOMER_ID" STRING,\n{4*chr(32)}"PRODUCT_ID" STRING'
    assert test_target_format == expected_target_format


@pytest.mark.usefixtures(
    "create_ddl_statement_params", "create_ddl_statement_targetddl"
)
def test_create_ddl_statement(
    create_ddl_statement_params, create_ddl_statement_targetddl
):
    test_target_ddl = create_ddl_without_transaction_payload_statement(
        create_ddl_statement_params[0],
        create_ddl_statement_params[1],
        create_ddl_statement_params[2],
        create_ddl_statement_params[3],
        create_ddl_statement_params[4],
    )
    expected_target_ddl = create_ddl_statement_targetddl
    assert test_target_ddl == expected_target_ddl
