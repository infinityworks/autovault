CREATE TABLE IF NOT EXISTS "$target_database"."$target_schema"."$versioned_source_name" (
    $keys_and_types_str,
    $payload_columns_and_types_str,
    "RECORD_SOURCE" STRING,
    "LOAD_DATETIME" TIMESTAMP_TZ
    );
$access_grants