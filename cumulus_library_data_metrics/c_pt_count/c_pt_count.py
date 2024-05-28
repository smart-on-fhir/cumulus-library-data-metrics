"""Module for generating c_pt_count tables"""

from typing import ClassVar

from cumulus_library.base_table_builder import BaseTableBuilder

from cumulus_library_data_metrics.base import MetricMixin


class PatientCountBuilder(MetricMixin, BaseTableBuilder):
    name = "c_pt_count"
    uses_fields: ClassVar[dict] = {
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
        self.queries = [self.render_sql(self.name, src="Patient")]
