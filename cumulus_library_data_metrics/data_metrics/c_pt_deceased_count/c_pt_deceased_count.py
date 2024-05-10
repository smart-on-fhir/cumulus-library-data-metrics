"""Module for generating c_pt_deceased_count tables"""

from cumulus_library.base_table_builder import BaseTableBuilder
from cumulus_library_data_metrics.data_metrics.base import MetricMixin


class DeceasedCountBuilder(MetricMixin, BaseTableBuilder):
    name = "c_pt_deceased_count"

    def add_metric_queries(self, *args, **kwargs) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_pt_deceased_count-demographics-count-of-deceased-patients-by-gender-by-age-at-death
        self.queries = [self.render_sql(self.name)]
