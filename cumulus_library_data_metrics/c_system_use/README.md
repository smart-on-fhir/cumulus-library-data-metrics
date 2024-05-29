# c_system_use

**Which Systems Are in Use?**

This metric makes a new table for each target resource & field combo,
slicing and dicing that field by category and time (if relevant).

### Fields

- category (depending on resource)
- year (depending on resource)
- status
- systems

### Notes on `systems`

To avoid double-counting, fields which have multiple systems
(either from the same `CodeableConcept` or an array of `CodeableConcepts`)
concatenate the systems together.

That is, if a single field has `snomed` and `icd10` systems,
it would be displayed as `icd10; snomed`.
