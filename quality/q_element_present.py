"""Module for generating q_element_present tables"""

import os.path

import jinja2

from cumulus_library.base_table_builder import BaseTableBuilder
from quality.base import MetricMixin


class ElementPresentBuilder(MetricMixin, BaseTableBuilder):
    name = "q_element_present"

    def make_table(self, **kwargs) -> str:
        """Make a single metric table"""
        summary_key = f"{kwargs['src'].lower()}_{kwargs['field'].lower().replace('.', '_')}"
        self.summary_entries[summary_key] = kwargs['src']

        return self.render_sql(self.name, **kwargs)

    def prepare_queries(self, *args, **kwargs) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_element_present-completeness-expect-element-to-be-populated
        # These are all fields flagged as Mandatory in a US Core profile.
        self.queries = [
            self.make_table(src="AllergyIntolerance", field="code"),
            self.make_table(src="AllergyIntolerance", field="patient"),
            self.make_table(src="AllergyIntolerance", field="reaction.manifestation"),
            # US Core has two Condition profiles, but both have the same mandatory fields
            # (note that we aren't checking for us-core category, to allow for non-profile rows)
            self.make_table(src="Condition", field="code"),
            self.make_table(src="Condition", field="subject"),
            self.make_table(src="Device", field="type"),
            self.make_table(src="DocumentReference", field="type"),
            self.make_table(src="Immunization", field="vaccineCode"),
            self.make_table(src="Medication", field="code"),
            # self.make_table(src="MedicationAdministration", field="medicationCodeableConcept"),
            self.make_table(src="MedicationRequest", field="medicationCodeableConcept"),
            self.make_table(src="Observation", field="code"),
            self.make_table(src="Observation", field="valueCodeableConcept"),
            self.make_table(src="Procedure", field="code"),
            self.make_summary(),
        ]
