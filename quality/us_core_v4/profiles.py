"""Module for generating tables based on US Core v4 profile features"""

from cumulus_library import databases
from cumulus_library.template_sql import base_templates

from quality.base import MetricMixin


class UsCoreV4Mixin(MetricMixin):

    # These methods largely deal with inspecting the schema before we fully query the table.
    # Complex column values deeper than the toplevel are not guaranteed to be present in the schema.
    # So we check if they are here.

    uses_fields = {
        "AllergyIntolerance": {
            "reaction": [
                "manifestation",
            ],
        },
        "DocumentReference": {
            "content": [
                "attachment",
                "format",
            ],
            "context": [
                "encounter",
                "period",
            ],
        },
        "Observation": {
            "component": [
                "dataAbsentReason",
                "valueCodeableConcept",
                "valuePeriod",
                "valueQuantity",
                "valueRange",
                "valueRatio",
                "valueSampledData",
            ],
            "effectiveTiming": [
                "code",
                "event",
                "repeat",
            ],
            "referenceRange": [
                "high",
                "low",
            ],
        },
        "Patient": {
            "communication": [
                "language",
            ],
            "extension": [
                # ideally would be able to go deeper for valueCoding.code/system, used by
                # race & ethnicity extensions. But just check a nested extension for now.
                "extension",
            ],
        },
    }

    @staticmethod
    def get_profile_name(kwargs: dict[str, str]) -> str:
        profile_name = kwargs["src"].lower()
        if "name" in kwargs:
            profile_name += f"_{kwargs['name']}"
        return profile_name

    def render_sql(self, template: str, **kwargs) -> str:
        if "src" in kwargs:
            kwargs["profile_name"] = self.get_profile_name(kwargs)
        return super().render_sql(template, **kwargs)

    def make_table(self, **kwargs) -> None:
        pass  # to be overridden

    def extra_schema_checks(self, cursor: databases.DatabaseCursor, schema: str) -> None:
        # Check if we have all the pieces of the extension we need
        query = base_templates.get_column_datatype_query(
            schema, "Patient", ["extension"],
        )
        cursor.execute(query)
        result = cursor.fetchone()[1]
        # TODO: use proper schema checking like other profiles, once we can go deeper down tree
        self.schemas["Patient"]["has_extension_codes"] = (
            self.schemas["Patient"]["extension"]["extension"]
            and "code" in result
            and "system" in result
        )

    def add_metric_queries(self) -> None:
        # Observation is so big, that if it falls over in Athena, let's know early.
        # So we run these first,
        # self.make_table(src="Observation", name="blood_pressure", loinc="85354-9")
        self.make_table(src="Observation", name="laboratory", category="laboratory")
        self.make_table(src="Observation", name="smoking_status", loinc="72166-2")
        self.make_table(src="Observation", name="vital_signs", category="vital-signs")

        # Rest of profiles
        self.make_table(src="AllergyIntolerance")
        self.make_table(src="Condition")
        self.make_table(src="DiagnosticReport", name="note")
        self.make_table(src="DocumentReference")
        self.make_table(src="Encounter")
        self.make_table(src="Immunization")
        self.make_table(src="Medication")
        self.make_table(src="MedicationRequest")
        self.make_table(src="Patient")
        self.make_table(src="Procedure")
