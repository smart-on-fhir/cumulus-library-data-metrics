# c_us_core_v4_count

**How deep is the support for US Core profiles?**

### Fields

- profile_support
- year (depending on resource)
- status

### Notes on `profile_support`

There are three values:
- `Mandatory & Must Support` (all mandatory checks passed and all "must support" elements were present)
- `Mandatory Only` (all mandatory checks passed but some "must support" elements were not present)
- `None` (not all mandatory checks passed)

### Notes on "Must Support" fields

Compliance of "must support" fields is tricky to automatically detect.
Per the [US Core spec](http://hl7.org/fhir/us/core/STU4/conformance-expectations.html#must-support-elements):

> In situations where information on a particular data element is not present and the
> reason for absence is unknown, US Core Responders **SHALL NOT** include the data
> elements in the resource instance returned as part of the query results.

So fields that are marked as "must support" might validly not be in the resulting FHIR export.

This metric only indicates whether it saw all the "must support" fields present.
But if it did not see those fields present,
that does not necessarily indicate a failure on the part of the server software's compliance.
The data may not be present in the first place.

### A note on profile mandatory checks

All the same profile-specific cautions in the `q_valid_us_core_v4` metric
apply here too for the mandatory checks.

### A note on the DocumentReference profile and "Must Support" fields

The DocumentReference profile requires support for `identifier`.

But since Cumulus ETL strips that field, this metric does not examine it.

### A note on the Encounter profile and "Must Support" fields

The Encounter profile requires support for `identifier`.

But since Cumulus ETL strips that field, this metric does not examine it.
