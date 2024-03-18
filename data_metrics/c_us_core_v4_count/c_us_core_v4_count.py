"""Module for generating c_us_core_v4_count tables"""

import jinja2
from cumulus_library.base_table_builder import BaseTableBuilder

from data_metrics.us_core_v4 import UsCoreV4Mixin


class UsCoreV4CountBuilder(UsCoreV4Mixin, BaseTableBuilder):
    name = "c_us_core_v4_count"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        self.queries.append(self.render_sql(self.name, **kwargs))