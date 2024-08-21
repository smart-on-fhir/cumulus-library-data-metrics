"""Module for generating q_system_use tables"""

import cumulus_library

from cumulus_library_data_metrics import systems
from cumulus_library_data_metrics.base import MetricMixin


class SystemUseBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "q_system_use"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        self.add_summary_entry(kwargs["src"], kwargs["field"])
        self.queries.append(self.render_sql(self.name, **kwargs))

    def add_metric_queries(self) -> None:
        self.make_table(
            src="AllergyIntolerance",
            field="code",
            systems=[systems.RXNORM, systems.SNOMED],
        )
        self.make_table(
            src="Condition",
            field="code",
            systems=[systems.ICD9CM, systems.ICD10CM, systems.SNOMED],
        )
        self.make_table(src="Device", field="type", systems=[systems.SNOMED])
        self.make_table(src="DiagnosticReport", field="code", systems=[systems.LOINC])
        self.make_table(
            src="DocumentReference", field="type", systems=[systems.LOINC, systems.NULL_FLAVOR]
        )
        self.make_table(
            src="Immunization",
            field="vaccineCode",
            # The FHIR spec also gives urn:oid:1.2.36.1.2001.1005.17 as an example,
            # but the US Core profile drops that suggestion in favor of only CVX.
            systems=[systems.CVX],
        )
        self.make_table(
            src="Medication",
            field="code",
            # The FHIR spec gives SNOMED as an example, but the US Core profile drops that
            # suggestion in favor of only RxNorm
            systems=[systems.RXNORM],
        )
        self.make_table(
            src="MedicationRequest",
            field="medicationCodeableConcept",
            # The FHIR spec gives SNOMED as an example, but the US Core profile drops that
            # suggestion in favor of only RxNorm
            systems=[systems.RXNORM],
        )
        self.make_table(src="Observation", field="code", systems=[systems.LOINC])
        self.make_table(
            src="Observation",
            field="valueCodeableConcept",
            # Base FHIR doesn't suggest anything specific here, but the Laboratory and
            # Smoking Status profiles both want SNOMED.
            systems=[systems.SNOMED],
        )
        self.make_table(
            src="Procedure",
            field="code",
            systems=[
                # Base FHIR only gives SNOMED as an example,
                # but the US Core v4 profile lists all these.
                systems.CPT,
                systems.LOINC,
                systems.SNOMED,
                "http://www.ada.org/cdt",
                "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
                "http://www.cms.gov/Medicare/Coding/ICD10",
            ],
        )
        self.make_summary(group_column="field")
