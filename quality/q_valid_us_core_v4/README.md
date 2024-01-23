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

### Denominator

All possible rows for the resource in question.

(e.g. `count(*) from condition`)

In the case of Observation profiles,
it's just the count of rows with the category in question.

### A note on Observation profiles

Unlike the other resources, which check all rows, Observations are kind of a wild
west where each row does not declare which profile it is _trying_ to be, and categories
aren't required. So it's really hard to ding any specific row for non-compliance.

Instead, we take the approach of fixing the category, then treating all rows of that
category as self-reported US Core rows, and check for compliance within the category.
This misses some "bad behavior" like smoking statuses without a category.
But is that non-compliant? Not technically?
It's just not a Smoking Profile row in the first place,
rather than being a non-compliant Smoking Profile row.
That kind of stuff can be left to a characterization metric.

We only check the categories for which profiles cover the whole category.
For example, `social-history` only has the smoking-status profile, so we don't bother
testing social-history. And `exam` has no profiles. Again, a characterization metric
can handle looking at those numbers better, whereas this metrics warns of non-compliance.

### Debugging

Each resource/field combo creates a table full of each row
that was flagged as an issue.

For example, for `Condition` a table named
`quality__q_valid_us_core_v4_condition` is created.

These tables hold the `id` and `status` for each flagged row,
to aid root cause analysis.

A future improvement: tag the specific reason _why_ a row was flagged.
