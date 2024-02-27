"""Module for generating c_resources_per_pt tables"""

from cumulus_library.base_table_builder import BaseTableBuilder
from quality.base import MetricMixin


class ResourcesPerPatientBuilder(MetricMixin, BaseTableBuilder):
    name = "c_resources_per_pt"

    def add_metric_queries(self) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_resources_per_pt-volume-distribution-of-unique-resources-per-patient-by-resource-type-by-category

        resources = {
            "AllergyIntolerance": {
                "field": "patient",
            },
            "Condition": {
                "field": "subject",
            },
            "Device": {
                "field": "patient",
            },
            "DiagnosticReport": {
                "field": "subject",
            },
            "DocumentReference": {
                "field": "subject",
            },
            "Encounter": {
                "field": "subject",
            },
            "Immunization": {
                "field": "patient",
            },
            "MedicationRequest": {
                "field": "subject",
            },
            "Observation": {
                "field": "subject",
            },
            "Procedure": {
                "field": "subject",
            },
            "ServiceRequest": {
                "field": "subject",
            },
        }

        self.queries.append(self.render_sql(self.name, resources=resources))
