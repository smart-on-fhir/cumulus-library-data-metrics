"""Module for generating q_ref_target_pop tables"""

import os.path

import jinja2


class MetricMixin:

    name = "base"

    def __init__(self):
        super().__init__()
        self.display_text = f"Creating {self.name} tables…"
        self.summary_entries = {}

    def make_summary(self) -> str:
        """Makes a summary table, from all the individual metric tables"""
        return self.render_sql("base.summary", entries=self.summary_entries, metric=self.name)

    @staticmethod
    def render_sql(template: str, **kwargs) -> str:
        path = os.path.dirname(__file__)
        with open(f"{path}/{template}.jinja") as file:
            sql = jinja2.Template(file.read()).render(**kwargs)
            # print(sql)
            return sql
