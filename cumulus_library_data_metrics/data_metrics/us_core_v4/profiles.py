"""Module for generating tables based on US Core v4 profile features"""

from typing import ClassVar

from cumulus_library_data_metrics.data_metrics.base import MetricMixin


class UsCoreV4Mixin(MetricMixin):
    # These methods largely deal with inspecting the schema before we fully query the table.
    # Complex column values deeper than the toplevel are not guaranteed to be present in the schema.
    # So we check if they are here.

    uses_fields: ClassVar[dict] = {
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
            "context": {
                "encounter": {},
                "period": {
                    "start": {},
                    "end": {},
                },
            },
        },
        "Encounter": {
            "hospitalization": [
                "dischargeDisposition",
            ],
            "location": [
                "location",
            ],
        },
        "Observation": {
            "component": [
                "dataAbsentReason",
                "valueCodeableConcept",
                "valuePeriod",
                "valueQuantity",  # TODO: need to expand this deeper
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
            "extension": {
                "extension": {
                    "url": {},
                    "valueCoding": [
                        "code",
                        "system",
                    ],
                },
                "url": {},
            },
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
