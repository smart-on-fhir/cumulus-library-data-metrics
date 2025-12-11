"""Module for generating c_us_core_v6_count tables"""

import cumulus_library

from cumulus_library_data_metrics.us_core_v6 import UsCoreV6Mixin


class UsCoreV6CountBuilder(UsCoreV6Mixin, cumulus_library.BaseTableBuilder):
    name = "c_us_core_v6_count"

    def make_table(self, **kwargs) -> None:
        # Some checks are duplicated between mandatory and must-support.
        # For example, some required binding checks are done on the mandatory side
        # for fields that are marked as must-support. And when checking must-support
        # validity, we always check binding there too. So this flags the jinja
        # to skip such duplicated checks, which might be confusing if you're looking
        # at a metric like this one with both mandatory and must-support fields.
        kwargs["skip_duplicated_mandatory_checks"] = True

        for kind in ["mandatory", "must_support"]:
            split_arg = f"{kind}_split"
            if self.output_mode == "cube" and split_arg in kwargs:
                table_max = kwargs[split_arg]
                self.queries += [
                    self.render_sql(kind, table_num=i + 1, table_max=table_max, **kwargs)
                    for i in range(table_max)
                ]
            else:
                self.queries.append(self.render_sql(kind, **kwargs))
