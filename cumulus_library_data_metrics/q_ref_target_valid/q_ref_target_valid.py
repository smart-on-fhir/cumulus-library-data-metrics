"""Module for generating q_ref_target_valid tables"""

from typing import ClassVar

import cumulus_library

from cumulus_library_data_metrics.base import MetricMixin


class TargetValidBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "q_ref_target_valid"

    uses_fields: ClassVar[dict] = {
        "DocumentReference": {
            "context": {
                "encounter": {},
            },
        },
    }

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        self.add_summary_entry(kwargs["src"], kwargs["dest"])
        self.queries.append(self.render_sql(self.name, **kwargs))

    def add_metric_queries(self) -> None:
        self.make_table(src="AllergyIntolerance", dest="Patient", field="patient")
        self.make_table(src="AllergyIntolerance", dest="Encounter", field="encounter")
        self.make_table(src="Condition", dest="Patient", field="subject")
        self.make_table(src="Condition", dest="Encounter", field="encounter")
        self.make_table(src="Device", dest="Patient", field="patient")
        self.make_table(src="DiagnosticReport", dest="Patient", field="subject")
        self.make_table(src="DiagnosticReport", dest="Encounter", field="encounter")
        self.make_table(src="DocumentReference", dest="Patient", field="subject")
        self.make_table(
            src="DocumentReference",
            dest="Encounter",
            field="context.encounter",
            is_array=True,
        )
        self.make_table(src="Encounter", dest="Patient", field="subject")
        self.make_table(src="Immunization", dest="Patient", field="patient")
        self.make_table(src="Immunization", dest="Encounter", field="encounter")
        self.make_table(src="MedicationRequest", dest="Patient", field="subject")
        self.make_table(src="MedicationRequest", dest="Encounter", field="encounter")
        self.make_table(src="Observation", dest="Patient", field="subject")
        self.make_table(src="Observation", dest="Encounter", field="encounter")
        self.make_table(src="Procedure", dest="Patient", field="subject")
        self.make_table(src="Procedure", dest="Encounter", field="encounter")
        self.make_summary(group_column="target")
