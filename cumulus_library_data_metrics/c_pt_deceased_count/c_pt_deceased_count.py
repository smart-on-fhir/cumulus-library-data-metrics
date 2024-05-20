"""Module for generating c_pt_deceased_count tables"""

from cumulus_library.base_table_builder import BaseTableBuilder

from cumulus_library_data_metrics.base import MetricMixin


class DeceasedCountBuilder(MetricMixin, BaseTableBuilder):
    name = "c_pt_deceased_count"

    def add_metric_queries(self, *args, **kwargs) -> None:
        self.queries = [self.render_sql(self.name)]
