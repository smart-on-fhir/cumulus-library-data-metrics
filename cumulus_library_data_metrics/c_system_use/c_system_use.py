"""Module for generating c_system_use tables"""

import cumulus_library

from cumulus_library_data_metrics import systems
from cumulus_library_data_metrics.base import MetricMixin

# Note that this CUBE is already very large / slow.
# Please do not add new columns to it.
# We already had to drop one planned column (has_text) from it due to performance.


class SystemUseBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "c_system_use"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        self.queries.append(self.render_sql(self.name, system_names=systems.NAMES, **kwargs))

    def add_metric_queries(self) -> None:
        self.make_table(src="Observation", field="code", use_category=True)
        self.make_table(src="Observation", field="valueCodeableConcept", use_category=True)
        self.make_table(src="AllergyIntolerance", field="code")
        self.make_table(src="Condition", field="code", use_category=True)
        self.make_table(src="Device", field="type")
        self.make_table(src="DiagnosticReport", field="code")
        self.make_table(src="DocumentReference", field="type")
        self.make_table(src="Encounter", field="class", is_coding=True)
        self.make_table(src="Encounter", field="type", is_array=True)
        self.make_table(src="Immunization", field="vaccineCode")
        self.make_table(src="Medication", field="code")
        self.make_table(src="MedicationRequest", field="medicationCodeableConcept")
        self.make_table(src="Procedure", field="code")
