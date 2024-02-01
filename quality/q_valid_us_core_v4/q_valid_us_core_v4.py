"""Module for generating q_valid_us_core_v4 tables"""

from cumulus_library.base_table_builder import BaseTableBuilder
from cumulus_library.databases import DatabaseCursor

from quality.base import MetricMixin
from quality.us_core_v4 import UsCoreV4Mixin


class ValidUsCoreV4Builder(UsCoreV4Mixin, MetricMixin, BaseTableBuilder):
    name = "q_valid_us_core_v4"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        summary_key = kwargs["src"].lower()
        if "name" in kwargs:
            summary_key += f"_{kwargs['name']}"

        self.summary_entries[summary_key] = self.render_sql("../us_core_v4/slice", **kwargs)

        self.queries.append(self.render_sql(self.name, **kwargs))

    def prepare_queries(self, cursor: DatabaseCursor, schema: str, *args, **kwargs) -> None:
        self.make_table(src="AllergyIntolerance", **self.allergy_args(cursor, schema))
        self.make_table(src="Condition")
        self.make_table(src="DiagnosticReport")
        self.make_table(src="DocumentReference", **self.docref_args(cursor, schema))
        self.make_table(src="Encounter")
        self.make_table(src="Immunization")
        self.make_table(src="Medication")
        self.make_table(src="MedicationRequest")
        # self.make_table(src="Observation", name="blood_pressure", loinc="85354-9", **self.obs_args(cursor, schema))
        self.make_table(src="Observation", name="laboratory", category="laboratory", **self.obs_args(cursor, schema))
        self.make_table(src="Observation", name="smoking_status", loinc="72166-2", **self.obs_args(cursor, schema))
        self.make_table(src="Observation", name="vital_signs", category="vital-signs", **self.obs_args(cursor, schema))
        self.make_table(src="Patient")
        self.make_table(src="Procedure")
        self.make_summary()
