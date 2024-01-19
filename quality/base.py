"""Module for generating q_ref_target_pop tables"""

import os.path
from typing import Optional

import jinja2


class MetricMixin:

    name = "base"
    uses_dates = False

    def __init__(self):
        super().__init__()
        self.display_text = f"Creating {self.name} tables…"
        self.summary_entries = {}

    def make_summary(self) -> str:
        """Makes a summary table, from all the individual metric tables"""
        return self.render_sql("../base.summary", entries=self.summary_entries, metric=self.name)

    @staticmethod
    def get_dates(resource: str) -> Optional[list[str]]:
        if resource == "AllergyIntolerance":
            return ["recordeddate", "onsetdatetime", "onsetperiod.start"]
        elif resource == "Condition":
            return ["recordeddate", "onsetdatetime", "onsetperiod.start"]
        elif resource == "DocumentReference":
            return ["date"]
        elif resource == "DiagnosticReport":
            return ["effectiveDateTime", "effectivePeriod.start"]
        elif resource == "Encounter":
            return ["period.start"]
        elif resource == "Immunization":
            return ["occurrenceDateTime"]
        elif resource == "MedicationRequest":
            return ["authoredOn"]
        elif resource == "Observation":
            return ["effectiveDateTime", "effectivePeriod.start", "effectiveInstant"]
        elif resource == "Procedure":
            return ["performedDateTime", "performedPeriod.start"]
        return None

    def render_sql(self, template: str, **kwargs) -> str:
        path = os.path.dirname(__file__)

        if self.uses_dates:
            kwargs["dates"] = self.get_dates(kwargs["src"])

        with open(f"{path}/{self.name}/{template}.jinja") as file:
            template = file.read()
            loader = jinja2.FileSystemLoader(path)
            env = jinja2.Environment(loader=loader).from_string(template)
            sql = env.render(**kwargs)
            # print(sql)
            return sql
