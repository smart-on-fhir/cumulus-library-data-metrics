"""Module for generating c_resources_per_pt tables"""

from cumulus_library.base_table_builder import BaseTableBuilder
from data_metrics import resource_info
from data_metrics.base import MetricMixin


class ResourcesPerPatientBuilder(MetricMixin, BaseTableBuilder):
    name = "c_resources_per_pt"

    def add_metric_queries(self) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_resources_per_pt-volume-distribution-of-unique-resources-per-patient-by-resource-type-by-category

        # The SQL wants to examine all the resources at once - so we don't do our normal metric
        # pattern of rendering the template once per resource.
        self.queries += [
            self.render_sql(
                self.name,
                patient_fields=resource_info.PATIENTS,
                categories=resource_info.CATEGORIES,
            ),
        ]
