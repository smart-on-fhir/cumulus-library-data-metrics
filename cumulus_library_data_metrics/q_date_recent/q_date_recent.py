"""
Module for generating q_date_recent tables
"""

from cumulus_library.base_table_builder import BaseTableBuilder

from cumulus_library_data_metrics.base import MetricMixin


class DateRecentBuilder(MetricMixin, BaseTableBuilder):
    name = "q_date_recent"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        summary_key = kwargs["src"].lower()
        self.summary_entries[summary_key] = None

        self.queries.append(self.render_sql(self.name, **kwargs))

    def add_metric_queries(self) -> None:
        for src, fields in self.date_fields.items():
            self.make_table(src=src, fields=fields)
        self.make_summary()
