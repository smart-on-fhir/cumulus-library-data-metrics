"""Sets study metadata"""

import cumulus_library

from cumulus_library_data_metrics.base import MetricMixin


class MetadataBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "meta"

    def add_date_query(self) -> None:
        # This is just a mapping of *START* dates - no mechanism for looking up end dates in
        # periods. But that's ... fine. Across the whole dataset, that's a small difference.
        self.queries.append(self.render_sql("dates", src_dates=self.date_fields))

    def add_version_query(self) -> None:
        self.queries.append(self.render_sql("version"))

    def add_metric_queries(self) -> None:
        self.add_date_query()
        self.add_version_query()
