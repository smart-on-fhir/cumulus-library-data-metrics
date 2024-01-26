"""Module for generating q_valid_us_core_v4 tables"""

import os

from cumulus_library.base_table_builder import BaseTableBuilder
from cumulus_library.databases import DatabaseCursor
from cumulus_library.template_sql import templates

from quality.base import MetricMixin


class ValidUsCoreV4Builder(MetricMixin, BaseTableBuilder):
    name = "q_valid_us_core_v4"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        summary_key = kwargs["src"].lower()
        if "name" in kwargs:
            summary_key += f"_{kwargs['name'].replace('-', '_')}"

        self.summary_entries[summary_key] = self.render_sql("../us_core_v4/slice", **kwargs)

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

        # TODO: add more tests for low-schema versions of Observation profiles
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
        self.make_table(src="AllergyIntolerance")
        self.make_table(src="Condition")
        self.make_table(src="DiagnosticReport")
        self.make_table(src="DocumentReference", **self.docref_args(cursor, schema))
        self.make_table(src="Encounter")
        self.make_table(src="Immunization")
        self.make_table(src="Medication")
        self.make_table(src="MedicationRequest")
        self.make_table(src="Observation", name="laboratory", category="laboratory", **self.obs_args(cursor, schema))
        self.make_table(src="Observation", name="smoking-status", loinc="72166-2", **self.obs_args(cursor, schema))
        self.make_table(src="Observation", name="vital-signs", category="vital-signs", **self.obs_args(cursor, schema))
        self.make_table(src="Patient")
        self.make_table(src="Procedure")
        self.make_summary()
