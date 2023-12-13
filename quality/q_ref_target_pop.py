"""Module for generating q_ref_target_pop tables"""

import os.path

import jinja2

from cumulus_library.base_table_builder import BaseTableBuilder
from quality.base import MetricMixin


class TargetPopBuilder(MetricMixin, BaseTableBuilder):
    name = "q_ref_target_pop"

    def make_table(self, **kwargs) -> str:
        """Make a single metric table"""
        summary_key = f"{kwargs['src'].lower()}_{kwargs['dest'].lower()}"
        self.summary_entries[summary_key] = kwargs['src']

        return self.render_sql(self.name, **kwargs)

    def prepare_queries(self, *args, **kwargs) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_ref_target_pop-conformance-expect-reference-target-to-be-populated
        self.queries = [
            self.make_table(src="AllergyIntolerance", dest="Patient", field="patient"),
            self.make_table(src="Condition", dest="Patient", field="subject"),
            self.make_table(src="Device", dest="Patient", field="patient"),
            self.make_table(src="DocumentReference", dest="Patient", field="subject"),
            self.make_table(src="Immunization", dest="Patient", field="patient"),
            self.make_table(src="MedicationRequest", dest="Patient", field="subject"),
            self.make_table(src="Observation", dest="Patient", field="subject"),
            self.make_table(src="Procedure", dest="Patient", field="subject"),
            self.make_summary(),
        ]
