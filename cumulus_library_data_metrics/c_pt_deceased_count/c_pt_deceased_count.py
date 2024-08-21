"""Module for generating c_pt_deceased_count tables"""

import cumulus_library

from cumulus_library_data_metrics.base import MetricMixin


class DeceasedCountBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "c_pt_deceased_count"

    def add_metric_queries(self, *args, **kwargs) -> None:
        self.queries = [self.render_sql(self.name)]
