"""Module for generating q_ref_target_valid tables"""

import os.path

import jinja2

from cumulus_library.base_table_builder import BaseTableBuilder


class TargetValidBuilder(BaseTableBuilder):
    display_text = "Creating q_ref_target_valid tables..."

    @staticmethod
    def make_table(**kwargs) -> str:
        """Extracts code system details as a standalone table"""
        path = os.path.dirname(__file__)
        with open(f"{path}/q_ref_target_valid.jinja") as file:
            return jinja2.Template(file.read()).render(**kwargs)

    def prepare_queries(self, *args, **kwargs) -> None:
        self.queries = [
            self.make_table(src="Condition", dest="Patient", field="subject"),
            self.make_table(src="Condition", dest="Encounter", field="encounter"),
            self.make_table(src="Procedure", dest="Patient", field="subject"),
            self.make_table(src="Procedure", dest="Encounter", field="encounter"),
        ]
