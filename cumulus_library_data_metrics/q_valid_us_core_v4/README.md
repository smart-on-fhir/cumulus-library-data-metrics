# q_valid_us_core_v4

**Are US Core profile requirements being met?**

### Numerator (flagged rows)

All resource rows that don't meet any one of the profile requirements.

Note that this metric assumes valid FHIR behavior.

That is, it only tests **additional** requirements on top of basic FHIR required fields.
If both the FHIR spec and a US Core profile says a field is mandatory,
this metric may not check for it
(though we do allow some overlapping checks,
because we mostly implement the checks in "Each xxx must have:" section,
which do repeat base FHIR requirements).

Instead, we focus on additional mandatory fields and profile business logic like
"if verification status is entered-in-error, clinical status SHALL NOT be present"
or binding restrictions (on References or Codings).

Things this simplifies:
- A lot of field checking
- Most need for schema inspection (i.e. no nested fields we care about)
- Checking every single Reference and CodeableConcept for FHIR validity.
  Instead, we just check for the presence of field at all.

That said: where it's easy, we will still check for basic fields.
We just aren't promising that.

A future improvement: a separate metric that checks for basic FHIR validity,
and we can then join against those tables here to unify both checks.

To repeat:
1. This metric validates all mandatory behavior that is unique to a profile.
2. This metric reserves the right to validates any mandatory behavior for
profile-required fields, even if it's in the base FHIR spec.
In an ideal world with infinite development resources,
we'd do a full FHIR validation for every mandatory profile field.
But instead, we check base FHIR rules on a best-effort basis.
3. This metric will never attempt to check any field or rule that isn't
required by a US Core profile.

#### Current base FHIR rules that we validate

- Codes with required bindings (like status fields) stay within them
- References should point to the correct resources

### Denominator

All possible rows for the resource in question.

(e.g. `count(*) from condition`)

In the case of Observation profiles,
it's just the count of rows with the category in question.

### A note on the DiagnosticReport profile

The DiagnosticReport profiles mark `presentedForm` as "Must Support".

But since Cumulus ETL strips these fields as possible PHI,
this metric does not examine them.

### A note on the DocumentReference profile

The DocumentReference profile requires one or both of `content.attachment.data`
and `content.attachment.url`.

But since Cumulus ETL strips these fields as PHI,
this metric does not require them.

### A note on Observation profiles

Unlike the other resources, which check all rows, Observations are kind of a wild
west where each row does not declare which profile it is _trying_ to be, and categories
aren't required. So it's really hard to ding any specific row for non-compliance.

Instead, for each Observation-based profile, we choose one defining trait, fix that,
and then only look at rows with that trait, assuming they should be for that profile.

For example for the base Laboratory profile,
we look at all rows with the `laboratory` category.
For the Smoking Status profile,
we look at all rows with a `72166-2` LOINC code.

### A note on the Patient profile

The Patient profile requires both `identifier` and `name`.

But since Cumulus ETL strips these fields as PHI,
this metric does not require them.

### Debugging

Each resource/field combo creates a table full of each row
that was flagged as an issue.

For example, for `Condition` a table named
`data_metrics__q_valid_us_core_v4_condition` is created.

These tables hold the `id` and `status` for each flagged row,
to aid root cause analysis.

A future improvement: tag the specific reason _why_ a row was flagged.
