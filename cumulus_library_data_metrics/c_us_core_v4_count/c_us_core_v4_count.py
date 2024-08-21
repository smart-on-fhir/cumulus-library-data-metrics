"""Module for generating c_us_core_v4_count tables"""

import cumulus_library

from cumulus_library_data_metrics.us_core_v4 import UsCoreV4Mixin


class UsCoreV4CountBuilder(UsCoreV4Mixin, cumulus_library.BaseTableBuilder):
    name = "c_us_core_v4_count"

    def make_table(self, **kwargs) -> None:
        # Some checks are duplicated between mandatory and must-support.
        # For example, some required binding checks are done on the mandatory side
        # for fields that are marked as must-support. And when checking must-support
        # validity, we always check binding there too. So this flags the jinja
        # to skip such duplicated checks, which might be confusing if you're looking
        # at a metric like this one with both mandatory and must-support fields.
        kwargs["skip_duplicated_mandatory_checks"] = True

        if self.output_mode == "cube" and "mandatory_split" in kwargs:
            kwargs["table_max"] = kwargs["mandatory_split"]
            self.queries += [
                self.render_sql("mandatory", table_num=i + 1, **kwargs)
                for i in range(kwargs["table_max"])
            ]
        else:
            self.queries.append(self.render_sql("mandatory", **kwargs))

        self.queries.append(self.render_sql("must_support", **kwargs))
