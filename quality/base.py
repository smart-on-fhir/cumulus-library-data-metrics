"""Module for generating q_ref_target_pop tables"""

import os.path
from typing import Optional

import jinja2
from cumulus_library import databases
from cumulus_library.template_sql import base_templates


class MetricMixin:

    name = "base"
    uses_fields = {}

    DATE_FIELDS = {
        "AllergyIntolerance": ["recordedDate", "onsetDateTime", "onsetPeriod.start"],
        "Condition": ["recordedDate", "onsetDateTime", "onsetPeriod.start"],
        "DocumentReference": ["date"],  # TODO: add context.period.start?
        "DiagnosticReport": ["effectiveDateTime", "effectivePeriod.start"],
        "Encounter": ["period.start"],
        "Immunization": ["occurrenceDateTime"],
        "MedicationRequest": ["authoredOn"],
        "Observation": ["effectiveDateTime", "effectivePeriod.start", "effectiveInstant"],
        "Procedure": ["performedDateTime", "performedPeriod.start"],
    }

    def __init__(self):
        super().__init__()
        self.display_text = f"Creating {self.name} tables…"
        self.summary_entries = {}
        self.queries = []
        self.schemas = {}

    def make_summary(self) -> None:
        """Makes a summary table, from all the individual metric tables"""
        sql = self.render_sql("../base.summary", entries=self.summary_entries, metric=self.name)
        self.queries.append(sql)

    def _query_schema(self, cursor: databases.DatabaseCursor, schema: str, parser: databases.DatabaseParser) -> None:
        for table, cols in self.uses_fields.items():
            query = base_templates.get_column_datatype_query(schema, table.lower(), cols.keys())
            cursor.execute(query)
            table_schema = cursor.fetchall()
            self.schemas[table] = parser.validate_table_schema(cols, table_schema)

    def extra_schema_checks(self, cursor: databases.DatabaseCursor, schema: str) -> None:
        pass

    def add_metric_queries(self) -> None:
        pass

    def prepare_queries(self, cursor: databases.DatabaseCursor, schema: str, *args, parser: databases.DatabaseParser, **kwargs) -> None:
        self._query_schema(cursor, schema, parser)
        self.extra_schema_checks(cursor, schema)
        self.add_metric_queries()

    def render_sql(self, template: str, **kwargs) -> str:
        path = os.path.dirname(__file__)

        if src := kwargs.get("src"):
            kwargs["dates"] = self.DATE_FIELDS.get(src)
            kwargs["schema"] = self.schemas.get(src)

        with open(f"{path}/{self.name}/{template}.jinja") as file:
            template = file.read()
            loader = jinja2.FileSystemLoader(path)
            env = jinja2.Environment(loader=loader).from_string(template)
            sql = env.render(**kwargs)
            # print(sql)
            return sql
