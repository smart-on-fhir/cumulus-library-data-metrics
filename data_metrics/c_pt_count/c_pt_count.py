"""Module for generating c_pt_count tables"""

from cumulus_library.base_table_builder import BaseTableBuilder
from cumulus_library.databases import DatabaseCursor
from cumulus_library.template_sql import base_templates

from data_metrics.base import MetricMixin


class PatientCountBuilder(MetricMixin, BaseTableBuilder):
    name = "c_pt_count"
    uses_fields = {
        "Patient": {
            "extension": {
                "extension": {
                    "url": {},
                    "valueCoding": [
                        "code",
                        "system",
                    ],
                },
                "url": {},
            },
        },
    }

    def add_metric_queries(self) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_pt_count-demographics-count-of-patients-by-birth-year-by-gender-by-ethnicity-by-race
        self.queries = [self.render_sql(self.name, src="Patient")]
