"""Module for generating q_ref_target_pop tables"""

from cumulus_library.base_table_builder import BaseTableBuilder

from cumulus_library_data_metrics.base import MetricMixin


class TargetPopBuilder(MetricMixin, BaseTableBuilder):
    name = "q_ref_target_pop"

    def make_table(self, **kwargs) -> str:
        """Make a single metric table"""
        summary_key = f"{kwargs['src'].lower()}_{kwargs['dest'].lower()}"
        self.summary_entries[summary_key] = None

        self.queries.append(self.render_sql(self.name, **kwargs))

    def add_metric_queries(self) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_ref_target_pop-conformance-expect-reference-target-to-be-populated
        self.make_table(src="AllergyIntolerance", dest="Patient", field="patient")
        self.make_table(src="Condition", dest="Patient", field="subject")
        self.make_table(src="Device", dest="Patient", field="patient")
        self.make_table(src="DiagnosticReport", dest="Patient", field="subject")
        self.make_table(src="DocumentReference", dest="Patient", field="subject")
        self.make_table(src="Encounter", dest="Patient", field="subject")
        self.make_table(src="Immunization", dest="Patient", field="patient")
        self.make_table(src="MedicationRequest", dest="Patient", field="subject")
        self.make_table(src="Observation", dest="Patient", field="subject")
        self.make_table(src="Procedure", dest="Patient", field="subject")
        self.make_summary()
