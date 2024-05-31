"""Module for generating c_us_core_v4_count tables"""

from cumulus_library.base_table_builder import BaseTableBuilder

from cumulus_library_data_metrics.us_core_v4 import UsCoreV4Mixin


class UsCoreV4CountBuilder(UsCoreV4Mixin, BaseTableBuilder):
    name = "c_us_core_v4_count"

    def make_table(self, **kwargs) -> None:
        if self.get_output_mode() == "cube" and "mandatory_split" in kwargs:
            kwargs["table_max"] = kwargs["mandatory_split"]
            self.queries += [
                self.render_sql("mandatory", table_num=i + 1, **kwargs)
                for i in range(kwargs["table_max"])
            ]
        else:
            self.queries.append(self.render_sql("mandatory", **kwargs))

        self.queries.append(self.render_sql("must_support", **kwargs))
