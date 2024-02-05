"""Module for generating q_valid_us_core_v4 tables"""

from cumulus_library.base_table_builder import BaseTableBuilder

from quality.us_core_v4 import UsCoreV4Mixin


class ValidUsCoreV4Builder(UsCoreV4Mixin, BaseTableBuilder):
    name = "q_valid_us_core_v4"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        profile_name = self.get_profile_name(kwargs)
        self.summary_entries[profile_name] = self.render_sql("../us_core_v4/slice", **kwargs)
        self.queries.append(self.render_sql(self.name, **kwargs))

    def prepare_queries(self, *args, **kwargs) -> None:
        super().prepare_queries(*args, **kwargs)
        self.make_summary()
