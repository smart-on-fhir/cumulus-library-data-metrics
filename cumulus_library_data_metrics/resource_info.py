"""Holds various static info about resources we want to examine."""

from cumulus_library_data_metrics import systems

# Categories to slice on
CATEGORIES = {
    "AllergyIntolerance": {
        "cat_field": "category",
    },
    "Condition": {
        "cat_field": "category",
        "cat_systems": [
            # https://hl7.org/fhir/us/core/stu4/ValueSet-us-core-condition-category.html
            systems.CONDITION_CATEGORY,
            [systems.USCORE_CONDITION_CATEGORY, ["health-concern"]],
            [systems.SNOMED, ["16100001"]],
        ],
    },
    "DiagnosticReport": {
        "cat_field": "category",
        # http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-diagnosticreport-lab.html
        # https://hl7.org/fhir/us/core/STU4/ValueSet-us-core-diagnosticreport-category.html
        "cat_systems": [
            [systems.DIAGNOSTIC_SECTION, ["LAB"]],  # for labs
            [systems.LOINC, ["LP29684-5", "LP29708-2", "LP7839-6"]],  # for notes
        ],
    },
    "DocumentReference": {
        "cat_field": "category",
        # https://hl7.org/fhir/us/core/STU4/ValueSet-us-core-documentreference-category.html
        "cat_systems": [systems.USCORE_DOCREF_CATEGORY],
    },
    "Encounter": {
        "cat_field": "class",
        # https://www.hl7.org/fhir/R4/v3/ActEncounterCode/vs.html
        "cat_systems": [systems.ENCOUNTER_CLASS],
        "is_coding": True,
    },
    "MedicationRequest": {
        "cat_field": "category",
        # http://hl7.org/fhir/R4/valueset-medicationrequest-category.html
        "cat_systems": [systems.MEDREQ_CATEGORY],
    },
    "Observation": {
        "cat_field": "category",
        # https://www.hl7.org/fhir/R4/valueset-observation-category.html
        "cat_systems": [systems.OBSERVATION_CATEGORY],
    },
}

# Date fields in preference order.
# This prefers "interaction with health system" dates, then administrative dates like "issued",
# then best effort start dates like onsetDateTime.
# See https://github.com/sync-for-science/qualifier/blob/master/metrics.md#by-date
DATES = {
    "AllergyIntolerance": ["recordedDate", "onsetDateTime", "onsetPeriod.start", "onsetPeriod.end"],
    "Condition": [
        "recordedDate",
        "onsetDateTime",
        "onsetPeriod.start",
        "onsetPeriod.end",
        "abatementDateTime",
        "abatementPeriod.start",
        "abatementPeriod.end",
    ],
    "DiagnosticReport": [
        "effectiveDateTime",
        "effectivePeriod.start",
        "effectivePeriod.end",
        "issued",
    ],
    "DocumentReference": ["context.period.start", "context.period.end", "date"],
    "Encounter": ["period.start", "period.end"],
    "Immunization": ["occurrenceDateTime", "recorded"],
    "MedicationRequest": ["authoredOn"],
    "Observation": [
        "effectiveDateTime",
        "effectivePeriod.start",
        "effectivePeriod.end",
        "effectiveInstant",
        "issued",
    ],
    "Procedure": ["performedDateTime", "performedPeriod.start", "performedPeriod.end"],
}

# Which field to examine for a Patient
PATIENTS = {
    "AllergyIntolerance": "patient",
    "Condition": "subject",
    "Device": "patient",
    "DiagnosticReport": "subject",
    "DocumentReference": "subject",
    "Encounter": "subject",
    "Immunization": "patient",
    "MedicationRequest": "subject",
    "Observation": "subject",
    "Procedure": "subject",
    "ServiceRequest": "subject",
}

SUPPORTED = {
    "AllergyIntolerance",
    "Condition",
    "Device",
    "DiagnosticReport",
    "DocumentReference",
    "Encounter",
    "Immunization",
    "Medication",
    "MedicationRequest",
    "Observation",
    "Patient",
    "Procedure",
}

# Use these in your metrics' "uses_fields" section when you want to inspect attachments.
# Usually with docref_utils.extract_attachments().
# Use like:
# uses_fields: ClassVar[dict] = {
#     "DiagnosticReport": {
#         **DIAGNOSTIC_REPORT_ATTACHMENT_SCHEMA,
#     },
#     "DocumentReference": {
#         **DOCREF_ATTACHMENT_SCHEMA,
#     },
# }
ATTACHMENT_SCHEMA = {
    "contentType": {},
    "language": {},
    "data": {},
    "_data": {
        "extension": {
            "url": {},
            "valueCode": {},
        },
    },
    "url": {},
    "_url": {
        "extension": {
            "url": {},
            "valueCode": {},
        },
    },
}
DIAGNOSTIC_REPORT_ATTACHMENT_SCHEMA = {
    "presentedForm": ATTACHMENT_SCHEMA,
}
DOCREF_ATTACHMENT_SCHEMA = {
    "content": {
        "attachment": ATTACHMENT_SCHEMA,
        "format": {
            "system": {},
            "code": {},
        },
    },
}
