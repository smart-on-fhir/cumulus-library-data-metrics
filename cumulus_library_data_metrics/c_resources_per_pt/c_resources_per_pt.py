"""Module for generating c_resources_per_pt tables"""

import cumulus_library

from cumulus_library_data_metrics import resource_info
from cumulus_library_data_metrics.base import MetricMixin


class ResourcesPerPatientBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "c_resources_per_pt"

    def add_metric_queries(self) -> None:
        # The SQL wants to examine all the resources at once - so we don't do our normal metric
        # pattern of rendering the template once per resource.
        self.queries += [
            self.render_sql(
                self.name,
                patient_fields=resource_info.PATIENTS,
                categories=resource_info.CATEGORIES,
            ),
        ]
