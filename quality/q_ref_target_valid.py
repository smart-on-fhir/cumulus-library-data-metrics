"""Module for generating q_ref_target_valid tables"""

import os.path

import jinja2

from cumulus_library.base_table_builder import BaseTableBuilder


class TargetValidBuilder(BaseTableBuilder):
    display_text = "Creating q_ref_target_valid tables..."

    def __init__(self):
        super().__init__()
        self.summary_entries = {}

    def make_table(self, **kwargs) -> str:
        """Extracts code system details as a standalone table"""
        summary_key = f"{kwargs['src'].lower()}_{kwargs['dest'].lower()}"
        self.summary_entries[summary_key] = {kwargs['src']: kwargs['dest']}

        path = os.path.dirname(__file__)
        with open(f"{path}/q_ref_target_valid.table.jinja") as file:
            sql = jinja2.Template(file.read()).render(**kwargs)
            # print(sql)
            return sql

    def make_summary(self) -> str:
        """Extracts code system details as a standalone table"""
        path = os.path.dirname(__file__)
        with open(f"{path}/q_ref_target_valid.summary.jinja") as file:
            sql = jinja2.Template(file.read()).render(entries=self.summary_entries)
            # print(sql)
            return sql

    def prepare_queries(self, *args, **kwargs) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_ref_target_valid-completeness-expect-reference-target-to-be-resolvable-when-populated
        self.queries = [
            self.make_table(src="AllergyIntolerance", dest="Patient", field="patient"),
            self.make_table(src="AllergyIntolerance", dest="Encounter", field="encounter"),
            self.make_table(src="Condition", dest="Patient", field="subject"),
            self.make_table(src="Condition", dest="Encounter", field="encounter"),
            self.make_table(src="Device", dest="Patient", field="patient"),
            self.make_table(src="DocumentReference", dest="Patient", field="subject"),
            self.make_table(src="DocumentReference", dest="Encounter", field="context.encounter", is_array=True),
            self.make_table(src="Immunization", dest="Patient", field="patient"),
            self.make_table(src="Immunization", dest="Encounter", field="encounter"),
            self.make_table(src="MedicationRequest", dest="Patient", field="subject"),
            self.make_table(src="MedicationRequest", dest="Encounter", field="encounter"),
            self.make_table(src="Observation", dest="Patient", field="subject"),
            self.make_table(src="Observation", dest="Encounter", field="encounter"),
            self.make_table(src="Procedure", dest="Patient", field="subject"),
            self.make_table(src="Procedure", dest="Encounter", field="encounter"),
            self.make_summary(),
        ]
