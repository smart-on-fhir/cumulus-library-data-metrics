# Contributing to Data Metrics

## Set up your dev environment

To use the same dev environment as us, you'll want to run these commands:
```sh
pip install .[dev]
pre-commit install
```

This will install dependencies & build tools,
as well as set up an auto-formatter commit hook.

## SQL Writing Guidelines
- Don't depend on `core__` tables.
  - Allows folks to build this study even if they can't or haven't built `core`
  - Allows `core` to smooth over data oddities we might be interested in

- For non-CUBE tables (like quality `q_` metric summaries or `c_resources_per_pt`),
  always try to have a `cumulus__all` row for the second grouping column,
  as well as the normal row -- which can hold the group value,
  be NULL if no grouping exists, or maybe `cumulus__none` if the row
  represents all resources without a group value.
  This way, downstream visualizers can reliably roll-up detailed views into
  more abstract views.
