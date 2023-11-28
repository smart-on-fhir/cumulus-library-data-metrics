# Quality Metrics

See [qualifier repo](https://github.com/sync-for-science/qualifier/blob/master/metrics.md)
for some metric definitions.


## SQL Writing Guidelines
- Don't depend on `core__` tables.
  - Allows folks to build this study even if they can't or haven't built `core`
  - Allows `core` to smooth over data oddities we might be interested in

- Consider looking at macros/logic from Google's analytics if helpful:
  - https://github.com/google/fhir-dbt-analytics

## Metric Prioritization

### Table stakes quality:
- `q_term_use` complies with US Core v1
- `q_ref_target_pop` complies with US Core v1 (can be run on partial extracts)
- `q_ref_target_valid` complies with US Core v1 (only on full extracts or data lake)
- `q_element_present` complies with US Core v1 element with min cardinality of 1

### Table stakes characterization:
- `c_resource_count` (by category, year, month)
- `c_pt_count` (by birth year gender, ethnicity, race)
- `c_pt_deceased_count` (by gender, by age at death)
- `c_term_coverage` (by resource type, by category)
- `c_resources_per_pt` (include combinations?)

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
