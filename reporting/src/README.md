# Cumulus Data Metrics Report

Visualizations of locally run FHIR data quality and characterization metrics

## Setup

1. Install [git](https://git-scm.com/downloads), [nodejs](https://nodejs.org) and [python](https://www.python.org/)

2. Clone this repository and switch to the `/reporting` subdirectory
    ```
    git clone {repository path}
    cd {repository name}/reporting
    ```

3. Install dependencies
    ```
    npm i
    ```

4. Ensure that the [Cumulus Data Metrics Library](https://github.com/smart-on-fhir/cumulus-library-data-metrics) is installed
    ```
    pip install cumulus-library-data-metrics
    ```


## Calculate Metrics

1. Follow the instructions outlined in the Cumulus Data Metrics Library [documentation](https://github.com/smart-on-fhir/cumulus-library-data-metrics). 

    When running metrics, be sure to specify a `db-type` of `duckdb`, a `database` named `output-tables.db` and set the `DATA_METRICS_OUTPUT_MODE` environment variable to `aggregate`. Your command should look something like this (with the path to your actual ndjson data):
    ```
    DATA_METRICS_OUTPUT_MODE=aggregate \
    cumulus-library build \
    --db-type duckdb \
    --database data/output-tables.db \
    --load-ndjson-dir {path/to/ndjson/root} \
    --target data_metrics
    ```

    Alternatively, metrics can be run on AWS Athena and metric tables can be exported to CSV and imported into a new DuckDB database at `data/output-tables.db`.

2. Once the metrics have run, launch the reporting server
    ```
    npm run dev
    ```

3. You can also build a static copy of the report which will generate html files in the `dist` directory that can be loaded onto any web server
    ```
    npm run build
    ```

## Updating and Customizing Reports

The metrics report is built with the open source [Observable Framework](https://observablehq.com/framework/getting-started) and has no other dependencies.