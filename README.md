# Data Metrics

A Cumulus-based implementation of the [qualifier metrics](https://github.com/sync-for-science/qualifier/blob/master/metrics.md).

## Implemented Metrics

The following qualifier metrics are implemented (per June 2024 qualifer definitions).

- [c_pt_count](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_pt_count)
- [c_pt_deceased_count](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_pt_deceased_count)
- [c_resource_count](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_resource_count)
- [c_resources_per_pt](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_resources_per_pt)
- [c_system_use](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_system_use)
- [c_us_core_v4_count](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_us_core_v4_count)
  - Note that the various more-specific Vital Signs profiles are not yet implemented
- [q_date_recent](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_date_recent)
- [q_ref_target_pop](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_ref_target_pop)
- [q_ref_target_valid](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_ref_target_valid)
- [q_system_use](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_system_use)
- [q_valid_us_core_v4](https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_valid_us_core_v4)
  - Note that the various more-specific Vital Signs profiles are not yet implemented

## Installing

```sh
pip install cumulus-library-data-metrics
```

## Running the Metrics

These metrics are designed as a
[Cumulus Library](https://docs.smarthealthit.org/cumulus/library/)
study and are run using the `cumulus-library` command.

### Local Ndjson
First, you'll want to organize your ndjson into the following file tree format:
```
root/
  condition/
    my-conditions.ndjson
  medicationrequest/
    1.ndjson
    2.ndjson
  patient/
    Patient.ndjson
```
(This is the same format that Cumulus ETL writes out when using `--output-format=ndjson`.)

Here's a sample command to run against that pile of ndjson data:
```sh
cumulus-library build \
  --db-type duckdb \
  --database output-tables.db \
  --load-ndjson-dir path/to/ndjson/root \
  --target data_metrics
```

And then you can load `output-tables.db` in a DuckDB session and see the results.
Or read below to export the counts tables.

### Athena
Here's a sample command to run against your Cumulus data in Athena:
```sh
cumulus-library build \
  --database your-glue-database \
  --workgroup your-athena-workgroup \
  --profile your-aws-credentials-profile \
  --target data_metrics
```

And then you can see the resulting tables in Athena.
Or read below to export the counts tables.

### Exporting Counts

For the metrics that have exportable counts (the characterization metrics mostly),
you can easily export those using Cumulus Library,
by replacing `build` in the above commands with `export ./output-folder`.
Like so:

```sh
cumulus-library export \
  ./output-folder \
  --db-type duckdb \
  --database output-tables.db \
  --target data_metrics
```

#### Aggregate counts

This study generates `CUBE` output by default.
If it's easier to work with simple aggregate counts of every value combination
(that is, without the partial value combinations that `CUBE()` generates),
run the build step with `DATA_METRICS_OUTPUT_MODE=aggregate` in your environment.

That is, run it like:
```sh
env \
  DATA_METRICS_OUTPUT_MODE=aggregate \
  cumulus-library build ...
```
