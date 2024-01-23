# q_ref_target_valid

**Do references point at an actual resource that exists?**

This looks at whether target reference resources actually exist.

For example, "for every `Condition.subject` that points to a patient,
does that target actual exist in the Patient database?"

### Numerator (flagged rows)

Any source Reference field which has a `.reference`
that looks like `"TargetResource/xxx"` but the corresponding `xxx` resource
does not actually exist.

Note that this does not check spec-valid but more complex forms like
absolute URLs, contained resources, logical references, or display-only references.
All such forms are not included in the numerator or denominator.

### Denominator

All fields for the resource in question that have a populated reference to
the target resource.

(e.g. `count(*) from condition where subject.reference like 'Patient/%'`)

### Debugging

Each resource/field combo creates a table full of each row
that was flagged as an issue.

For example, for `Condition.subject` a table named
`quality__q_ref_target_valid_condition_subject` is created.

These tables hold the `id`, `status`, and problem field for each flagged row,
to aid root cause analysis.
