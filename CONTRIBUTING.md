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
