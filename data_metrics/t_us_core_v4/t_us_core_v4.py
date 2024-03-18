"""Fake/test metric for us_core_v4 profiles"""

import jinja2
from cumulus_library.base_table_builder import BaseTableBuilder

from data_metrics.us_core_v4 import UsCoreV4Mixin


class TestUsCoreV4Builder(UsCoreV4Mixin, BaseTableBuilder):
    name = "t_us_core_v4"

    def make_table(self, **kwargs) -> None:
        """Make a table for both mandatory and must_support"""
        # Keep these separate to make it easier to tell the many valid_* fields apart in the
        # "expected" csv files.
        self.queries.append(self.render_sql("mandatory", **kwargs))
        try:
            self.queries.append(self.render_sql("must_support", **kwargs))
        except jinja2.exceptions.TemplateNotFound:
            pass  # remove this try/except once we have must-support enabled for all profiles
