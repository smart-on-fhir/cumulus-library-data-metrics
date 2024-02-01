"""Module for generating c_us_core_v4_count tables"""

from cumulus_library.base_table_builder import BaseTableBuilder
from cumulus_library.databases import DatabaseCursor

from quality.base import MetricMixin
from quality.us_core_v4 import UsCoreV4Mixin


class UsCoreV4CountBuilder(UsCoreV4Mixin, MetricMixin, BaseTableBuilder):
    name = "c_us_core_v4_count"
    uses_dates = True

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        self.queries.append(self.render_sql(self.name, **kwargs))

    # TODO: expand to more profiles
    def prepare_queries(self, cursor: DatabaseCursor, schema: str, *args, **kwargs) -> None:
        self.make_table(src="AllergyIntolerance", **self.allergy_args(cursor, schema))
        self.make_table(src="Condition")
