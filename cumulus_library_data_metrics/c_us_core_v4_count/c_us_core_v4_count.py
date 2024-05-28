"""Module for generating c_us_core_v4_count tables"""

from cumulus_library.base_table_builder import BaseTableBuilder

from cumulus_library_data_metrics.us_core_v4 import UsCoreV4Mixin


class UsCoreV4CountBuilder(UsCoreV4Mixin, BaseTableBuilder):
    name = "c_us_core_v4_count"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        self.queries += [
            # We break these into two tables to keep CUBE sizes reasonable.
            self.render_sql("mandatory", **kwargs),
            self.render_sql("must_support", **kwargs),
        ]
