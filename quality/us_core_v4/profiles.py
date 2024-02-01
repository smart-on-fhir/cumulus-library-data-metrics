"""Module for generating tables based on US Core v4 profile features"""

from cumulus_library.databases import DatabaseCursor
from cumulus_library.template_sql import templates


class UsCoreV4Mixin:

    @staticmethod
    def allergy_args(cursor: DatabaseCursor, schema: str) -> dict:
        query = templates.get_column_datatype_query(
            schema, "allergyintolerance", ["reaction"],
        )
        cursor.execute(query)
        result = cursor.fetchone()[1]
        return {
            "has_manifestation": "manifestation" in result,
        }

    @staticmethod
    def docref_args(cursor: DatabaseCursor, schema: str) -> dict:
        # We need to see if the content.attachment structure exists in the source
        # because our SQL wants to reference it, but it's deeper than Cumulus's default
        # schema depth of one, so it may not be in the schema.
        query = templates.get_column_datatype_query(
            schema, "documentreference", ["content"],
        )
        cursor.execute(query)
        result = cursor.fetchone()[1]
        return {
            "has_attachment": "attachment" in result,
        }

    @staticmethod
    def obs_args(cursor: DatabaseCursor, schema: str) -> dict:
        # Check referenceRange.* fields
        query = templates.get_column_datatype_query(
            schema, 'observation', ['referencerange'],
        )
        cursor.execute(query)
        ref_range_result = cursor.fetchone()[1]

        # Check component.* fields
        query = templates.get_column_datatype_query(
            schema, 'observation', ['component'],
        )
        cursor.execute(query)
        comp_result = cursor.fetchone()[1].lower()

        # TODO: add more tests for low-schema versions of Observation profiles
        return {
            "has_ref_range_high": "high" in ref_range_result,
            "has_ref_range_low": "low" in ref_range_result,
            "has_comp_data_absent": "dataabsentreason" in comp_result,
            "has_comp_quantity": "valuequantity" in comp_result,
            "has_comp_concept": "valuecodeableconcept" in comp_result,
            "has_comp_range": "valuerange" in comp_result,
            "has_comp_ratio": "valueratio" in comp_result,
            "has_comp_sample": "valuesampleddata" in comp_result,
            "has_comp_period": "valueperiod" in comp_result,
        }
