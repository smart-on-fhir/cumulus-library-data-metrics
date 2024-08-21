"""Module for generating q_valid_us_core_v4 tables"""

import cumulus_library

from cumulus_library_data_metrics.us_core_v4 import UsCoreV4Mixin


class ValidUsCoreV4Builder(UsCoreV4Mixin, cumulus_library.BaseTableBuilder):
    name = "q_valid_us_core_v4"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        self.add_summary_entry(
            kwargs["src"],
            kwargs.get("name"),
            denominator=self.render_sql("../us_core_v4/slice", **kwargs),
        )
        self.queries.append(self.render_sql(self.name, **kwargs))

    def add_metric_queries(self) -> None:
        super().add_metric_queries()
        self.make_summary(group_column="profile")
