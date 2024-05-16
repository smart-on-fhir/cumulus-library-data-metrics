"""Module for generating q_ref_target_pop tables"""

import copy
import os.path
from typing import ClassVar

import jinja2
from cumulus_library import base_utils
from cumulus_library.template_sql import sql_utils

from cumulus_library_data_metrics import resource_info


class MetricMixin:
    name = "base"
    uses_fields: ClassVar[dict] = {}

    def __init__(self):
        super().__init__()
        self.display_text = f"Creating {self.name} tables…"
        self.summary_entries = {}
        self.queries = []
        self.schemas = {}

        # These date fields are mostly static, but may be modified when checking the schema if
        # some of them are not present (notably DocRef.context.period.start).
        self.date_fields = copy.deepcopy(resource_info.DATES)

    def make_summary(self) -> None:
        """Makes a summary table, from all the individual metric tables"""
        sql = self.render_sql("../base.summary", entries=self.summary_entries, metric=self.name)
        self.queries.append(sql)

    def _query_schema(self, config: base_utils.StudyConfig) -> None:
        fields_to_check = copy.deepcopy(self.uses_fields)

        # Since so many metrics use date data, add a standard date field into the mix
        check_docref_period = "context.period.start" in self.date_fields["DocumentReference"]
        if check_docref_period:
            docref = fields_to_check.setdefault("DocumentReference", {})
            context = docref.setdefault("context", {})
            period = context.setdefault("period", {})
            period["start"] = {}

        self.schemas = sql_utils.validate_schema(config.db, fields_to_check)

        if (
            check_docref_period
            and not self.schemas["DocumentReference"]["context"]["period"]["start"]
        ):
            self.date_fields["DocumentReference"].remove("context.period.start")

    def extra_schema_checks(self, config: base_utils.StudyConfig) -> None:
        pass

    def add_metric_queries(self) -> None:
        pass

    def prepare_queries(
        self,
        *args,
        config: base_utils.StudyConfig,
        **kwargs,
    ) -> None:
        self._query_schema(config)
        self.extra_schema_checks(config)
        self.add_metric_queries()

    def render_sql(self, template: str, **kwargs) -> str:
        path = os.path.dirname(__file__)

        if src := kwargs.get("src"):
            kwargs["dates"] = self.date_fields.get(src)
            kwargs["patient_field"] = resource_info.PATIENTS.get(src)
            kwargs["schema"] = self.schemas.get(src)
            kwargs.update(resource_info.CATEGORIES.get(src, {}))

        # See how we should combine counts.
        # TODO: add the ability for cumulus-library to take study args like
        #  --study-option=output-mode:cube (or whatever)
        output_mode = os.environ.get("DATA_METRICS_OUTPUT_MODE")
        if output_mode not in {"aggregate", "cube"}:
            output_mode = "cube"
        kwargs["output_mode"] = output_mode

        with open(f"{path}/{self.name}/{template}.jinja") as file:
            template = file.read()
            loader = jinja2.FileSystemLoader(path)
            env = jinja2.Environment(loader=loader).from_string(template)
            sql = env.render(**kwargs)
            # print(sql)
            return sql
