# c_term_coverage

**Which Systems Are in Use?**

This metric makes a new table for each target resource & field combo,
slicing and dicing that field by category and time (if relevant).

### Fields

- category (depending on resource)
- has_text (depending on field)
- year (depending on resource)
- status
- systems

### Notes on `has_text`

This metric looks only at `CodeableConcept.text`,
not any `Coding.display` values inside the `CodeableConcept`.

There are four values:
- `cumulus__none` (no `CodeableConcepts` were present at all for the field)
- `No Text` (none of the `CodeableConcepts` have text)
- `Partial Text` (some of the `CodeableConcepts` in the array had text, others did not)
- `Has Text` (all `CodeableConcepts` for the field had text)

### Notes on `systems`

To avoid double-counting, fields which have multiple systems
(either from the same `CodeableConcept` or an array of `CodeableConcepts`)
concatenate the systems together.

That is, if a single field has `snomed` and `icd10` systems,
it would be displayed as `icd10; snomed`.
