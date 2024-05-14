# q_date_recent

**Are dates in the plausibly "recent" past?**

### Numerator (flagged rows)

Any row for which any of its date fields are outside our target range.

The earliest a date can still be "plausible" is 1900-01-01
(which is arbitrary, but BCH sees reasonable dates as far back as 1915
for backdated near-birth events like allergy onsets).

The latest a date can be is the current time.

Rows with an `entered-in-error` status
(or Encounters with a `planned` status)
are ignored.

### Denominator

All possible rows for the resource in question.

(e.g. `count(*) from condition`)

### Debugging

Each resource/field combo creates a table full of each row
that was flagged as an issue.

For example, for `Condition.subject` a table named
`data_metrics__q_date_recent_condition` is created.

These tables hold the `id`, `status`, and date fields for each flagged row,
to aid root cause analysis.
