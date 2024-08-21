"""
Module for generating q_date_recent tables
"""

import cumulus_library

from cumulus_library_data_metrics.base import MetricMixin


class DateRecentBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "q_date_recent"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        self.add_summary_entry(kwargs["src"])
        self.queries.append(self.render_sql(self.name, **kwargs))

    def add_metric_queries(self) -> None:
        for src, fields in self.date_fields.items():
            self.make_table(src=src, fields=fields)
        self.make_summary()
