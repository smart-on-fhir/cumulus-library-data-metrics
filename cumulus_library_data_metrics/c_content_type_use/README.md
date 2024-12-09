# c_content_type_use

**Count of resources by attachment content types**

### Fields

- status
- doc_status
- year
- type
- content_types

### Notes on `doc_status`

This field is always `cumulus__none` on resources that don't support it,
like `DiagnosticReport`.

### Notes on `type`

This field pulls from different FHIR fields depending on the resource.
It holds `DiagnosticReport.code` and `DocumentReference.type`.

These type values are not yet converted to display values.
They are just presented as the raw `code` value.
