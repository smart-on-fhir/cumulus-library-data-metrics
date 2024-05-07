"""Module for generating c_resources_per_pt tables"""

from cumulus_library.base_table_builder import BaseTableBuilder
from data_metrics.base import MetricMixin
from data_metrics import resource_info

class ResourcesPerPatientBuilder(MetricMixin, BaseTableBuilder):
    name = "c_resources_per_pt"

    def add_metric_queries(self) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_resources_per_pt-volume-distribution-of-unique-resources-per-patient-by-resource-type-by-category

        self.queries.append(self.render_sql(self.name, resources=resource_info.PATIENTS))
