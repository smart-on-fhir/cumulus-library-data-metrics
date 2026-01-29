"""Module for generating tables based on US Core v6 profile features"""

from typing import ClassVar

from cumulus_library_data_metrics import resource_info
from cumulus_library_data_metrics.base import MetricMixin


class UsCoreV6Mixin(MetricMixin):
    # These methods largely deal with inspecting the schema before we fully query the table.
    # Complex column values deeper than the toplevel are not guaranteed to be present in the schema.
    # So we check if they are here.

    uses_fields: ClassVar[dict] = {
        "AllergyIntolerance": {
            "reaction": [
                "manifestation",
            ],
        },
        "Condition": {
            "extension": [
                "url",
                "valueDateTime",
            ],
        },
        "DiagnosticReport": {
            "media": [
                "link",
            ],
        },
        "DocumentReference": {
            "context": {
                "encounter": {},
                "period": {
                    "start": {},
                    "end": {},
                },
            },
            **resource_info.DOCREF_ATTACHMENT_SCHEMA,
        },
        "Encounter": {
            "participant": [
                "type",
                "period",
                "individual",
            ],
            "hospitalization": [
                "dischargeDisposition",
            ],
            "location": [
                "location",
            ],
        },
        "MedicationRequest": {
            "dosageInstruction": {
                "timing": {},
                "doseAndRate": {
                    "doseQuantity": [
                        "system",
                    ],
                    "doseRange": {
                        "low": [
                            "system",
                        ],
                        "high": [
                            "system",
                        ],
                    },
                },
            },
            "dispenseRequest": [
                "quantity",
            ],
        },
        "Observation": {
            "component": {
                "dataAbsentReason": {},
                "valueCodeableConcept": {},
                "valuePeriod": {},
                "valueQuantity": [
                    "value",
                    "comparator",
                    "unit",
                    "system",
                    "code",
                ],
                "valueRange": {},
                "valueRatio": {},
                "valueSampledData": {},
            },
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
                    "valueCodeableConcept": {},
                    "valueCoding": [
                        "code",
                        "system",
                    ],
                },
                "url": {},
                "valueCodeableConcept": {},
            },
        },
    }

    def render_sql(self, template: str, **kwargs) -> str:
        if src := kwargs.get("src"):
            kwargs["profile_name"] = self.make_table_fragment(src, kwargs.get("name"))
        return super().render_sql(template, **kwargs)

    def make_table(self, **kwargs) -> None:
        pass  # to be overridden

    def add_metric_queries(self) -> None:
        # Common kwargs:
        # - src: FHIR resource
        # - name: subcategory of profile, used in table names
        # - category/loinc: property to slice on for Observations
        # - *_split: some profiles have a lot of fields, which can cause performance issues when
        #   cubing. This is a recommended hint of how many tables to split any cube into.
        #   Note that this argument gets passed on to the metric classes that implement this mixin,
        #   and _optionally_ used. For example, the q_valid_us_core_v6 metric does not care about
        #   this argument, because it doesn't cube.
        #   The c_us_core_v6_count metric *does* care about it, when cubing. It will split its
        #   output tables into multiple tables, to keep CUBE time low.
        #   The recommendation is to split a profile such that each table's field count is <= 4.
        #   This ends up meaning the final table will have 6 fields or less, because fields like
        #   status or year may get added.

        # Observation is so big, that if it falls over in Athena, let's know early.
        # So we run these first,
        self.make_table(
            src="Observation",
            name="Laboratory",
            category="laboratory",
            mandatory_split=2,
            must_support_split=2,
        )
        self.make_table(
            src="Observation", name="Smoking Status", loinc="72166-2", mandatory_split=2
        )
        self.make_table(
            src="Observation", name="Vital Signs", category="vital-signs", mandatory_split=3
        )

        # Rest of profiles
        self.make_table(src="AllergyIntolerance")
        self.make_table(src="Condition", name="Enc", must_support_split=2)
        self.make_table(src="Condition", name="Prob", must_support_split=2)
        self.make_table(src="DiagnosticReport", name="Lab")
        self.make_table(src="DiagnosticReport", name="Note", must_support_split=2)
        self.make_table(src="DocumentReference", mandatory_split=2, must_support_split=2)
        self.make_table(src="Encounter", must_support_split=2)
        self.make_table(src="Immunization")
        self.make_table(src="Medication")
        self.make_table(src="MedicationRequest", mandatory_split=2, must_support_split=3)
        self.make_table(src="Patient", must_support_split=3)
        self.make_table(src="Procedure")
