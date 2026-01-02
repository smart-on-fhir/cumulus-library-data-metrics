"""Module for generating q_date_in_lifetime tables"""

import cumulus_library

from cumulus_library_data_metrics.base import MetricMixin
from cumulus_library_data_metrics.resource_info import DATES


class TargetPopBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "q_date_in_lifetime"

    def make_table(self, **kwargs) -> None:
        self.add_summary_entry(kwargs["src"])
        self.queries.append(self.render_sql(self.name, **kwargs))

    def add_metric_queries(self) -> None:
        for resource in DATES:
            self.make_table(src=resource)
        self.make_summary()
