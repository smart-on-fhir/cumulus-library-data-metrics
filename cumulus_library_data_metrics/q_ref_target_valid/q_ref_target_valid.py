"""Module for generating q_ref_target_valid tables"""

from typing import ClassVar

import cumulus_library

from cumulus_library_data_metrics.base import MetricMixin


class TargetValidBuilder(MetricMixin, cumulus_library.BaseTableBuilder):
    name = "q_ref_target_valid"

    uses_fields: ClassVar[dict] = {
        "DocumentReference": {
            "context": {
                "encounter": {},
            },
        },
        "Encounter": {
            "participant": {
                "individual": {},
            },
            "location": {
                "location": {},
            },
        },
        "Patient": {
            "link": {
                "other": {},
            },
        },
    }

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        self.add_summary_entry(kwargs["src"], f"{kwargs['field']}:{kwargs['dest']}")
        self.queries.append(self.render_sql(self.name, **kwargs))

    def add_metric_queries(self) -> None:
        self.make_table(src="AllergyIntolerance", dest="Patient", field="patient")
        self.make_table(src="AllergyIntolerance", dest="Encounter", field="encounter")
        self.make_table(src="Condition", dest="Patient", field="subject")
        self.make_table(src="Condition", dest="Encounter", field="encounter")
        self.make_table(src="Device", dest="Patient", field="patient")
        self.make_table(src="DiagnosticReport", dest="Patient", field="subject")
        self.make_table(src="DiagnosticReport", dest="Encounter", field="encounter")
        self.make_table(
            src="DiagnosticReport", dest="Organization", field="performer", is_array=True
        )
        self.make_table(
            src="DiagnosticReport", dest="Practitioner", field="performer", is_array=True
        )
        self.make_table(src="DiagnosticReport", dest="Observation", field="result", is_array=True)
        self.make_table(src="DocumentReference", dest="Patient", field="subject")
        self.make_table(src="DocumentReference", dest="Practitioner", field="author", is_array=True)
        self.make_table(
            src="DocumentReference",
            dest="Encounter",
            field="context.encounter",
            is_array=True,
        )
        self.make_table(src="Encounter", dest="Patient", field="subject")
        self.make_table(
            src="Encounter", dest="Practitioner", field="participant.individual", parent_array=True
        )
        self.make_table(src="Encounter", dest="Condition", field="reasonReference", is_array=True)
        self.make_table(
            src="Encounter", dest="Location", field="location.location", parent_array=True
        )
        self.make_table(src="Encounter", dest="Organization", field="serviceProvider")
        self.make_table(src="Immunization", dest="Patient", field="patient")
        self.make_table(src="Immunization", dest="Encounter", field="encounter")
        self.make_table(src="Location", dest="Organization", field="managingOrganization")
        self.make_table(src="MedicationRequest", dest="Practitioner", field="reportedReference")
        self.make_table(src="MedicationRequest", dest="Medication", field="medicationReference")
        self.make_table(src="MedicationRequest", dest="Patient", field="subject")
        self.make_table(src="MedicationRequest", dest="Encounter", field="encounter")
        self.make_table(src="MedicationRequest", dest="Practitioner", field="requester")
        self.make_table(
            src="MedicationRequest", dest="Condition", field="reasonReference", is_array=True
        )
        self.make_table(
            src="MedicationRequest", dest="Observation", field="reasonReference", is_array=True
        )
        self.make_table(src="Observation", dest="Patient", field="subject")
        self.make_table(src="Observation", dest="Organization", field="performer", is_array=True)
        self.make_table(src="Observation", dest="Patient", field="performer", is_array=True)
        self.make_table(src="Observation", dest="Practitioner", field="performer", is_array=True)
        self.make_table(
            src="Observation", dest="PractitionerRole", field="performer", is_array=True
        )
        self.make_table(src="Observation", dest="Encounter", field="encounter")
        self.make_table(src="Observation", dest="Observation", field="hasMember", is_array=True)
        self.make_table(
            src="Observation", dest="DocumentReference", field="derivedFrom", is_array=True
        )
        self.make_table(src="Observation", dest="Observation", field="derivedFrom", is_array=True)
        self.make_table(src="Patient", dest="Patient", field="link.other", parent_array=True)
        self.make_table(src="PractitionerRole", dest="Practitioner", field="practitioner")
        self.make_table(src="PractitionerRole", dest="Organization", field="organization")
        self.make_table(src="PractitionerRole", dest="Location", field="location", is_array=True)
        self.make_table(src="Procedure", dest="Patient", field="subject")
        self.make_table(src="Procedure", dest="Encounter", field="encounter")
        self.make_summary(group_column="target")
