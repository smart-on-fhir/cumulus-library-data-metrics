"""Fake/test metric for us_core_v4 profiles"""

import cumulus_library

from cumulus_library_data_metrics.us_core_v4 import UsCoreV4Mixin


class TestUsCoreV4Builder(UsCoreV4Mixin, cumulus_library.BaseTableBuilder):
    name = "t_us_core_v4"

    def make_table(self, **kwargs) -> None:
        """Make a table for both mandatory and must_support"""
        # Keep these separate to make it easier to tell the many valid_* fields apart in the
        # "expected" csv files.
        self.queries.append(self.render_sql("mandatory", **kwargs))
        self.queries.append(self.render_sql("must_support", **kwargs))
