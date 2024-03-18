"""Module for generating q_ref_target_valid tables"""

from cumulus_library.base_table_builder import BaseTableBuilder
from quality.base import MetricMixin


class TargetValidBuilder(MetricMixin, BaseTableBuilder):
    name = "q_ref_target_valid"

    uses_fields = {
        "DocumentReference": {
            "context": [
                "encounter",
            ],
        },
    }

    def make_table(self, **kwargs) -> str:
        """Make a single metric table"""
        summary_key = f"{kwargs['src'].lower()}_{kwargs['dest'].lower()}"

        # Only count filled-in references, not every row
        self.summary_entries[summary_key] = self.render_sql(f"denominator", **kwargs)

        self.queries.append(self.render_sql(self.name, **kwargs))

    def add_metric_queries(self) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_ref_target_valid-completeness-expect-reference-target-to-be-resolvable-when-populated
        self.make_table(src="AllergyIntolerance", dest="Patient", field="patient"),
        self.make_table(src="AllergyIntolerance", dest="Encounter", field="encounter"),
        self.make_table(src="Condition", dest="Patient", field="subject"),
        self.make_table(src="Condition", dest="Encounter", field="encounter"),
        self.make_table(src="Device", dest="Patient", field="patient"),
        self.make_table(src="DiagnosticReport", dest="Patient", field="subject"),
        self.make_table(src="DiagnosticReport", dest="Encounter", field="encounter"),
        self.make_table(src="DocumentReference", dest="Patient", field="subject"),
        self.make_table(src="DocumentReference", dest="Encounter", field="context.encounter", is_array=True),
        self.make_table(src="Immunization", dest="Patient", field="patient"),
        self.make_table(src="Immunization", dest="Encounter", field="encounter"),
        self.make_table(src="MedicationRequest", dest="Patient", field="subject"),
        self.make_table(src="MedicationRequest", dest="Encounter", field="encounter"),
        self.make_table(src="Observation", dest="Patient", field="subject"),
        self.make_table(src="Observation", dest="Encounter", field="encounter"),
        self.make_table(src="Procedure", dest="Patient", field="subject"),
        self.make_table(src="Procedure", dest="Encounter", field="encounter"),
        self.make_summary()
