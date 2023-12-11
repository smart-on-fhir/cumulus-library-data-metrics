"""Module for generating c_term_coverage tables"""

from cumulus_library.base_table_builder import BaseTableBuilder
from quality.base import MetricMixin


class TermCoverageBuilder(MetricMixin, BaseTableBuilder):
    name = "c_term_coverage"
    uses_dates = True

    def make_table(self, **kwargs) -> str:
        """Make a single metric table"""
        return self.render_sql(self.name, **kwargs)

    def prepare_queries(self, *args, **kwargs) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_term_coverage-terminology-count-of-resources-by-terminology-system-by-resource-type-by-category
        self.queries = [
            self.make_table(src="AllergyIntolerance", field="code"),
            self.make_table(
                src="Condition",
                field="code",
                category_system="http://terminology.hl7.org/CodeSystem/condition-category",
            ),
            self.make_table(src="Device", field="type"),
            self.make_table(src="DocumentReference", field="type"),
            self.make_table(src="Encounter", field="class", is_coding=True),
            self.make_table(src="Encounter", field="type", is_array=True),
            self.make_table(src="Immunization", field="vaccineCode"),
            self.make_table(src="Medication", field="code"),
            self.make_table(src="MedicationRequest", field="medicationCodeableConcept"),
            self.make_table(
                src="Observation",
                field="code",
                category_system="http://terminology.hl7.org/CodeSystem/observation-category",
            ),
            self.make_table(
                src="Observation",
                field="valueCodeableConcept",
                category_system="http://terminology.hl7.org/CodeSystem/observation-category",
            ),
            self.make_table(src="Procedure", field="code"),
        ]
