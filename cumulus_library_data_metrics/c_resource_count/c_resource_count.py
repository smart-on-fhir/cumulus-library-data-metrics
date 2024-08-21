"""Module for generating c_resource_count tables"""

import cumulus_library

from cumulus_library_data_metrics import resource_info
from cumulus_library_data_metrics.base import MetricMixin


class ResourceCountBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "c_resource_count"

    def make_tables(self, src: str) -> None:
        """Make metric tables"""
        if src in self.date_fields:
            self.queries.append(self.render_sql(self.name, period="month", src=src))
            self.queries.append(self.render_sql(self.name, period="year", src=src))
        else:
            # no date fields, so don't do separate periods
            self.queries.append(self.render_sql(self.name, period="all", src=src))

    def add_metric_queries(self) -> None:
        for resource in resource_info.SUPPORTED:
            self.make_tables(resource)
