"""Module for generating tables based on US Core v4 profile features"""

from cumulus_library.databases import DatabaseCursor
from cumulus_library.template_sql import templates


class UsCoreV4Mixin:

    # These methods largely deal with inspecting the schema before we fully query the table.
    # Complex column values deeper than the toplevel are not guaranteed to be present in the schema.
    # So we check if they are here.

    @staticmethod
    def _get_datatype(cursor: DatabaseCursor, schema: str, resource: str, column: str) -> str:
        query = templates.get_column_datatype_query(
            schema, resource.lower(), [column.lower()],
        )
        cursor.execute(query)
        return cursor.fetchone()[1].lower()

    @staticmethod
    def allergy_args(cursor: DatabaseCursor, schema: str) -> dict:
        reaction = UsCoreV4Mixin._get_datatype(cursor, schema, "AllergyIntolerance", "reaction")
        return {
            "has_manifestation": "manifestation" in reaction,
        }

    @staticmethod
    def docref_args(cursor: DatabaseCursor, schema: str) -> dict:
        content = UsCoreV4Mixin._get_datatype(cursor, schema, "DocumentReference", "content")
        context = UsCoreV4Mixin._get_datatype(cursor, schema, "DocumentReference", "context")
        return {
            "has_attachment": "attachment" in content,
            "has_format": "format" in content,
            "has_encounter": "encounter" in context,
            "has_period": "period" in context,
        }

    @staticmethod
    def obs_args(cursor: DatabaseCursor, schema: str) -> dict:
        ref_range = UsCoreV4Mixin._get_datatype(cursor, schema, "Observation", "referenceRange")
        component = UsCoreV4Mixin._get_datatype(cursor, schema, "Observation", "component")

        # TODO: add more tests for low-schema versions of Observation profiles
        return {
            "has_ref_range_high": "high" in ref_range,
            "has_ref_range_low": "low" in ref_range,
            "has_comp_data_absent": "dataabsentreason" in component,
            "has_comp_quantity": "valuequantity" in component,
            "has_comp_concept": "valuecodeableconcept" in component,
            "has_comp_range": "valuerange" in component,
            "has_comp_ratio": "valueratio" in component,
            "has_comp_sample": "valuesampleddata" in component,
            "has_comp_period": "valueperiod" in component,
        }
