{% docs $versioned_source_name_desc %}

# $versioned_source_name
$table_description

The original business process that generated the data is: $unit_of_work

## Source
- Name: $source_name
- Version: $version
- System: CRM_SYSTEM
- Freshness: $freshness
- Format: $format
- Filetype: $filetype

## Accessibility
- Raw source location: $source_location
- Database location: $database_location
- Database role access: $access_roles

### Access requests
$access_requests

## Quality
$quality
{% enddocs %}

{% docs $versioned_source_name_col_1 %}
$versioned_source_name_col_1_desc
{% enddocs %}

{% docs $versioned_source_name_col_2 %}
$versioned_source_name_col_2_desc
{% enddocs %}
