# Quality Metrics

See [qualifier repo](https://github.com/sync-for-science/qualifier/blob/master/metrics.md)
for some metric definitions.


## SQL Writing Guidelines
- Don't depend on `core__` tables.
  - Allows folks to build this study even if they can't or haven't built `core`
  - Allows `core` to smooth over data oddities we might be interested in

- Consider looking at macros/logic from Google's analytics if helpful:
  - https://github.com/google/fhir-dbt-analytics

## Differences from Original Qualifier Metrics

Across the board, we have some minor differences from the
[upstream metric definitions](https://github.com/sync-for-science/qualifier/blob/master/metrics.md):
- We usually stratify a metric by status as well as other fields
- We drop MedicationAdministration from our metrics - it's not really supported in Cumulus
- We add support for DiagnosticReport where sensible
- We consider Observation.effectivePeriod.start and Observation.effectiveInstant in addition
  to Observation.effectiveDateTime

Other specific deltas will be noted in the code for the given metric.

## Metric Prioritization

### Table stakes quality:
- `q_term_use` complies with US Core v1
- `q_ref_target_pop` complies with US Core v1 (can be run on partial extracts)
- `q_ref_target_valid` complies with US Core v1 (only on full extracts or data lake)
- `q_valid_us_core_v4`
  - numerator: resources that don't have all mandatory bits of any profile

### Table stakes characterization:
- `c_resource_count` (by category, year, month)
- `c_pt_count` (by birth year gender, ethnicity, race)
- `c_pt_deceased_count` (by gender, by age at death)
- `c_term_coverage` (by resource type, by category)
- `c_resources_per_pt` (include combinations?)
- `c_us_core_v4_count`
  - Tells how many rows match mandatory US Core support
  - And for each separate must-support requirement, tells which rows have the value

### High value quality:
- `q_date_sequence`
- `q_date_in_lifetime`
- `q_date_recent`

### High value characterization:
- `c_element_use` for USCDI v1 “must support” elements
- `c_date_precision` (by resource type, by category, by date element, by precision level)
- `c_identifier_coverage` (by resource type)

### Useful quality:
- `q_obs_value_range`
- `q_obs_comp_value_range`
