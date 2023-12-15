"""
Module for generating q_valid_us_core_v4 tables

Note that this metric assumes valid FHIR behavior.

That is, it only tests ADDITIONAL requirements on top of basic FHIR required fields.
If both the FHIR spec and a US Core profile says a field is mandatory, this metric
does not check for it.

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

    def make_table(self, **kwargs) -> str:
        """Make a single metric table"""
        summary_key = kwargs["src"].lower()
        if "category" in kwargs:
            summary_key += f"_{kwargs['category']}"
        self.summary_entries[summary_key] = kwargs["src"]

        return self.render_sql(self.name, **kwargs)

    @staticmethod
    def docref_args(cursor: DatabaseCursor, schema: str) -> dict:
        # We need to see if the content.attachment structure exists in the source
        # because our SQL wants to reference it, but it's deeper than Cumulus's default
        # schema depth of one, so it may not be in the schema.
        query = templates.get_column_datatype_query(
            schema, 'documentreference', 'content',
        )
        cursor.execute(query)
        result = cursor.fetchone()[0]
        has_attachment = "attachment" in result
        return {
            'has_attachment': has_attachment,
        }

    def prepare_queries(self, cursor: DatabaseCursor, schema: str, *args, **kwargs) -> None:
        self.queries = [
            self.make_table(src="AllergyIntolerance"),
            self.make_table(src="Condition"),
            self.make_table(src="DiagnosticReport"),
            self.make_table(src="DocumentReference", **self.docref_args(cursor, schema)),
            self.make_table(src="Encounter"),
            self.make_table(src="Immunization"),
            self.make_table(src="Medication"),
            self.make_table(src="MedicationRequest"),
            # Unlike the other resources, which check all rows, Observations are kind of a wild
            # west where each row does not declare which profile it is TRYING to be, and categories
            # aren't required and are US Core specific instead of FHIR specific. So it's really
            # hard to ding any specific row for non-compliance.
            # Instead, we take the approach of fixing the category, then treating all rows of that
            # category as self-reported US Core rows, and check for compliance within the category.
            # This misses some "bad behavior" like smoking statuses without a category.
            # But :shrug: is that non-compliant? Not technically?
            # That kind of stuff can be left to a characterization metric.
            self.make_table(src="Observation", category="laboratory"),
            self.make_summary(),
        ]
