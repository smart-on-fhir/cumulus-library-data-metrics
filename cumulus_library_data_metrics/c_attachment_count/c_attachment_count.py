"""Module for generating c_attachment_count tables"""

from typing import ClassVar

import cumulus_library

from cumulus_library_data_metrics import resource_info
from cumulus_library_data_metrics.base import MetricMixin


# Survey of attachments themselves
# e.g. How many attachments have extra info like language and format?
class AttachmentsCountBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "c_attachment_count"
    uses_fields: ClassVar[dict] = {
        "DiagnosticReport": {
            **resource_info.DIAGNOSTIC_REPORT_ATTACHMENT_SCHEMA,
        },
        "DocumentReference": {
            **resource_info.DOCREF_ATTACHMENT_SCHEMA,
        },
    }

    def add_metric_queries(self) -> None:
        self.queries.append(self.render_sql(self.name, src="DiagnosticReport"))
        self.queries.append(self.render_sql(self.name, src="DocumentReference"))
