"""Module for generating q_ref_target_pop tables"""

import copy
import os.path
import sys
from typing import ClassVar

import cumulus_library
import jinja2
from cumulus_library.template_sql import sql_utils

from cumulus_library_data_metrics import resource_info


class MetricMixin:
    name = "base"
    uses_fields: ClassVar[dict] = {}

    def __init__(self):
        super().__init__()
        self.display_text = f"Creating {self.name} tables…"
        self.study_prefix = "data_metrics"
        self.output_mode = "cube"
        self.summary_entries = {}
        # A "group" is a value in the second column - a secondary characteristic like "field"
        # (group examples: "code", "valueCodeableConcept") or a stratifier like "profile"
        # (group examples: "Lab", "Note"). These will "roll-up" to the resource level in the
        # summary with a "cumulus__all" group entry row.
        self.summary_groups = {}
        self.queries = []
        self.schemas = {}

        # These date fields are mostly static, but may be modified when checking the schema if
        # some of them are not present (notably DocRef.context.period.start).
        self.date_fields = copy.deepcopy(resource_info.DATES)

    def make_table_fragment(self, src: str, group: str | None = None):
        key = src.lower()
        if group:
            key += f"_{group.lower().replace(' ', '_')}"
        return key

    def add_summary_entry(
        self, src: str, group: str | None = None, *, denominator: str | None = None
    ) -> None:
        # These are all flags for the summary-table-builder jinja.
        key = self.make_table_fragment(src, group)
        self.summary_entries[key] = {
            "src": src,
            "group": group,
            "denominator": denominator,
        }
        self.summary_groups.setdefault(src, set()).add(group)

    def make_summary(self, group_column: str | None = None) -> None:
        """Makes a summary table, from all the individual metric tables"""
        # Always define *something* even if we don't use it, so that consuming visualizations
        # can assume a consistent two-column definition of resource + group.
        group_column = group_column or "subgroup"
        sql = self.render_sql(
            "../base.summary",
            entries=self.summary_entries,
            group_column=group_column,
            group_values=self.summary_groups,
            metric=self.name,
        )
        self.queries.append(sql)

    def _check_for_deep_docref_date(self, field: str, fields_to_check: dict) -> bool:
        check_docref_period = f"context.period.{field}" in self.date_fields["DocumentReference"]
        if check_docref_period:
            docref = fields_to_check.setdefault("DocumentReference", {})
            context = docref.setdefault("context", {})
            period = context.setdefault("period", {})
            period[field] = {}
        return check_docref_period

    def _clear_deep_docref_date(self, field: str) -> None:
        if not self.schemas["DocumentReference"]["context"]["period"][field]:
            self.date_fields["DocumentReference"].remove(f"context.period.{field}")

    def _query_schema(self, config: cumulus_library.StudyConfig) -> None:
        fields_to_check = copy.deepcopy(self.uses_fields)

        # Check for some known deep fields especially - if the list of fields grows, we should
        # make this more generic.
        check_docref_start = self._check_for_deep_docref_date("start", fields_to_check)
        check_docref_end = self._check_for_deep_docref_date("end", fields_to_check)

        self.schemas = sql_utils.validate_schema(config.db, fields_to_check)

        if check_docref_start:
            self._clear_deep_docref_date("start")
        if check_docref_end:
            self._clear_deep_docref_date("end")

    def extra_schema_checks(self, config: cumulus_library.StudyConfig) -> None:
        pass

    def add_metric_queries(self) -> None:
        pass

    def prepare_queries(
        self,
        *args,
        config: cumulus_library.StudyConfig,
        manifest: cumulus_library.StudyManifest,
        **kwargs,
    ) -> None:
        self.study_prefix = manifest.get_study_prefix()
        self.output_mode = self.get_output_mode(config)
        self._query_schema(config)
        self.extra_schema_checks(config)
        self.add_metric_queries()

    def get_output_mode(self, config: cumulus_library.StudyConfig) -> str:
        output_mode = (
            config.options.get("output-mode")
            # Deprecated approach (before --option existed) -- let it lie for now
            or os.environ.get("DATA_METRICS_OUTPUT_MODE")
        )
        if output_mode not in {"aggregate", "cube"}:
            if output_mode:
                print(
                    f"Did not understand output mode '{output_mode}'. Using 'cube' instead.",
                    file=sys.stderr,
                )
            output_mode = "cube"
        return output_mode

    def render_sql(self, template: str, **kwargs) -> str:
        path = os.path.dirname(__file__)

        if src := kwargs.get("src"):
            kwargs["dates"] = self.date_fields.get(src)
            kwargs["patient_field"] = resource_info.PATIENTS.get(src)
            kwargs["schema"] = self.schemas.get(src)
            kwargs.update(resource_info.CATEGORIES.get(src, {}))

        # See how we should combine counts.
        kwargs["output_mode"] = self.output_mode
        kwargs["study_prefix"] = self.study_prefix

        with open(f"{path}/{self.name}/{template}.jinja") as file:
            template = file.read()
            loader = jinja2.FileSystemLoader(path)
            env = jinja2.Environment(loader=loader).from_string(template)  # noqa: S701
            sql = env.render(**kwargs)
            # print(sql)
            return sql
