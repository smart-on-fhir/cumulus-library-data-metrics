"""
Module for generating q_valid_us_core_v4 tables

Note that this metric assumes valid FHIR behavior.

That is, it only tests ADDITIONAL requirements on top of basic FHIR required fields.
If both the FHIR spec and a US Core profile says a field is mandatory, this metric
may not check for it (though we do allow some overlapping checks, because we mostly
implement the checks in "Each xxx must have:" section, which do repeat base FHIR requirements.

Instead, we focus on additional mandatory fields and Profile business logic like
"if verification status is entered-in-error, clinical status SHALL NOT be present"
or binding restrictions (on References or Codings)

Things this simplifies:
- A lot of field checking
- Most need for schema inspection (i.e. no nested fields we care about)
- Checking every single Reference and CodeableConcept for FHIR validity.
  Instead, we just check for the presence of field at all.

That said: where it's easy, we will still check for basic fields.
We just aren't promising that.

A future improvement: a separate metric that checks for basic FHIR validity,
and we can then join against those tables here to unify both checks.
"""

from cumulus_library.base_table_builder import BaseTableBuilder
from cumulus_library.databases import DatabaseCursor
from cumulus_library.template_sql import templates

from quality.base import MetricMixin


class ValidUsCoreV4Builder(MetricMixin, BaseTableBuilder):
    name = "q_valid_us_core_v4"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        summary_key = kwargs["src"].lower()
        summary_denominator = kwargs["src"]
        if "category" in kwargs:
            self.queries.append(self.render_sql(f"{summary_key}_denominator", **kwargs))
            summary_key += f"_{kwargs['category'].replace('-', '_')}"
            # Setting None will tell the summary generator code to look at our pre-defined table
            summary_denominator = None

        self.summary_entries[summary_key] = summary_denominator
        self.queries.append(self.render_sql(self.name, **kwargs))

    @staticmethod
    def docref_args(cursor: DatabaseCursor, schema: str) -> dict:
        # We need to see if the content.attachment structure exists in the source
        # because our SQL wants to reference it, but it's deeper than Cumulus's default
        # schema depth of one, so it may not be in the schema.
        query = templates.get_column_datatype_query(
            schema, 'documentreference', ['content'],
        )
        cursor.execute(query)
        result = cursor.fetchone()[1]
        return {
            'has_attachment': "attachment" in result,
        }

    @staticmethod
    def obs_args(cursor: DatabaseCursor, schema: str) -> dict:
        # Check referenceRange.* fields
        query = templates.get_column_datatype_query(
            schema, 'observation', ['referencerange'],
        )
        cursor.execute(query)
        ref_range_result = cursor.fetchone()[1]

        # Check component.* fields
        query = templates.get_column_datatype_query(
            schema, 'observation', ['component'],
        )
        cursor.execute(query)
        comp_result = cursor.fetchone()[1]

        return {
            "has_ref_range_high": "high" in ref_range_result,
            "has_ref_range_low": "low" in ref_range_result,
            "has_comp_data_absent": "dataabsentreason" in comp_result,
            "has_comp_quantity": "valuequantity" in comp_result,
            "has_comp_concept": "valuecodeableconcept" in comp_result,
            "has_comp_range": "valuerange" in comp_result,
            "has_comp_ratio": "valueratio" in comp_result,
            "has_comp_sample": "valuesampleddata" in comp_result,
            "has_comp_period": "valueperiod" in comp_result,
        }

    def prepare_queries(self, cursor: DatabaseCursor, schema: str, *args, **kwargs) -> None:
        self.make_table(src="Condition")
        self.make_table(src="AllergyIntolerance")
        self.make_table(src="DiagnosticReport")
        self.make_table(src="DocumentReference", **self.docref_args(cursor, schema))
        self.make_table(src="Encounter")
        self.make_table(src="Immunization")
        self.make_table(src="Medication")
        self.make_table(src="MedicationRequest")

        # Unlike the other resources, which check all rows, Observations are kind of a wild
        # west where each row does not declare which profile it is TRYING to be, and categories
        # aren't required. So it's really hard to ding any specific row for non-compliance.
        #
        # Instead, we take the approach of fixing the category, then treating all rows of that
        # category as self-reported US Core rows, and check for compliance within the category.
        # This misses some "bad behavior" like smoking statuses without a category.
        # But :shrug: is that non-compliant? Not technically?
        # That kind of stuff can be left to a characterization metric.
        #
        # We only check the categories for which profiles cover the whole category.
        # For example, 'social-history' only has the smoking-status profile, so we don't bother
        # testing social-history. And 'exam' has no profiles. Again, a characterization metric
        # can handle looking at those numbers better, whereas this is warning of non-compliance.
        self.make_table(src="Observation", category="laboratory", **self.obs_args(cursor, schema))
        self.make_table(src="Observation", category="vital-signs", **self.obs_args(cursor, schema))
        # FIXME: add tests for vital-signs and/or confirm with Jamie the best way to slice this up.
        #  He was recommending a code-based approach instead of category-based.
        # FIXME: add more tests for low-schema versions of Observations

        self.make_table(src="Patient")
        self.make_table(src="Procedure")
        self.queries.append(self.make_summary())
