# q_ref_target_pop

**Are required references populated?**

This looks at whether certain required references to other resources exist.
It does _not_ confirm if the external referenced resource exists.
(That's `q_ref_target_valid`.)

For example, "does every `Condition.subject` point to a Patient resource?"

### Numerator (flagged rows)

Any row whose Reference field in question does _not_ have a `.reference`
that looks like `"TargetResource/xxx"` (i.e. does not have a relative reference
for the correct resource).

Note that this does not allow spec-valid but more complex forms like
absolute URLs, contained resources, logical references, or display-only references.

All such forms are counted in the numerator as problems.
It would be a possible improvement to tolerate such forms,
but for now we take the quick and dirty approach
(which also has the benefit of flagging a situation that could cause issues
elsewhere in Cumulus, which largely only supports relative references).

### Denominator

All possible rows for the resource in question.

(e.g. `count(*) from condition`)

### Debugging

Each resource/field combo creates a table full of each resource
that was flagged as an issue.

For example, for `Condition.subject` a table named
`data_metrics__q_ref_target_pop_condition_subject` is created.

These tables hold the `id`, `status`, and problem field for each flagged row,
to aid root cause analysis.
