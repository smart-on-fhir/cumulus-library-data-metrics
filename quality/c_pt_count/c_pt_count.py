"""Module for generating c_pt_count tables"""

from cumulus_library.base_table_builder import BaseTableBuilder
from cumulus_library.databases import DatabaseCursor
from cumulus_library.template_sql import base_templates

from quality.base import MetricMixin


class PatientCountBuilder(MetricMixin, BaseTableBuilder):
    name = "c_pt_count"

    @staticmethod
    def extension_args(cursor: DatabaseCursor, schema: str) -> dict:
        # Check if we have all the pieces of the extension we need
        query = base_templates.get_column_datatype_query(
            schema, "patient", ["extension"],
        )
        cursor.execute(query)
        result = cursor.fetchone()[1]
        # TODO: be way more fancy with this, with cumulus-library 2.0 and its schema stuff
        return {
            "has_extension_codes": "code" in result and "system" in result,
        }

    def prepare_queries(self, cursor: DatabaseCursor, schema: str, *args, **kwargs) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_pt_count-demographics-count-of-patients-by-birth-year-by-gender-by-ethnicity-by-race
        self.queries = [self.render_sql(self.name, **self.extension_args(cursor, schema))]
