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
- Warehouse location: $warehouse_location
- Warehouse role access: $access_roles

### Access requests
$access_requests

#### Maintained by
Data set maintained by: $maintained_by

## Quality & Known Issues
$quality
{% enddocs %}
