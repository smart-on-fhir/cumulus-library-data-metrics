"""Module for generating q_term_use tables"""

import os.path

import jinja2

from cumulus_library.base_table_builder import BaseTableBuilder
from quality.base import MetricMixin


class TermUseBuilder(MetricMixin, BaseTableBuilder):
    name = "q_term_use"

    def make_table(self, **kwargs) -> str:
        """Make a single metric table"""
        summary_key = f"{kwargs['src'].lower()}_{kwargs['field'].lower()}"
        self.summary_entries[summary_key] = kwargs['src']

        return self.render_sql(self.name, **kwargs)

    def prepare_queries(self, *args, **kwargs) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_term_use-conformance-expect-common-terminology-systems-to-be-populated
        self.queries = [
            self.make_table(src="AllergyIntolerance", field="code", system="http://snomed.info/sct"),
            self.make_table(src="Condition", field="code", system="http://snomed.info/sct"),
            self.make_table(src="Device", field="type", system="http://snomed.info/sct"),
            self.make_table(src="DocumentReference", field="type", system="http://loinc.org"),
            self.make_table(src="Immunization", field="vaccineCode", system="http://hl7.org/fhir/sid/cvx"),
            self.make_table(src="Medication", field="code", system="http://www.nlm.nih.gov/research/umls/rxnorm"),
            self.make_table(src="MedicationRequest", field="medicationCodeableConcept", system="http://www.nlm.nih.gov/research/umls/rxnorm"),
            self.make_table(src="Observation", field="code", system="http://loinc.org"),
            self.make_table(src="Observation", field="valueCodeableConcept", system="http://snomed.info/sct"),
            self.make_table(src="Procedure", field="code", system="http://www.ama-assn.org/go/cpt"),
            self.make_summary(),
        ]
