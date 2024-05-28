# q_system_use

**Are the recommended coding systems being used?**

### Numerator (flagged rows)

All resource rows that have codings without a recommended system.

A row with no codings is fine (not flagged/included in the numerator).
A row with multiple systems is also fine,
as long as one of them is a recommended one.

### Denominator

All possible rows for the resource in question.

(e.g. `count(*) from condition`)

### Debugging

Each resource/field combo creates a table full of each row
that was flagged as an issue.

For example, for `Condition.code` a table named
`data_metrics__q_system_use_condition_code` is created.

These tables hold the `id`, `status`, and problem field for each flagged row,
to aid root cause analysis.
