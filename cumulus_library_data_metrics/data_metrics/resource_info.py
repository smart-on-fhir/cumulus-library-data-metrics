"""Holds various static info about resources we want to examine."""

# Categories to slice on
CATEGORIES = {
    "AllergyIntolerance": {
        "cat_field": "category",
    },
    "Condition": {
        "cat_field": "category",
        "cat_systems": ["http://terminology.hl7.org/CodeSystem/condition-category"],
    },
    "DiagnosticReport": {
        "cat_field": "category",
        "cat_systems": [
            "http://loinc.org",
            "http://terminology.hl7.org/CodeSystem/v2-0074",
        ],
    },
    "DocumentReference": {
        "cat_field": "category",
        "cat_systems": [
            "http://hl7.org/fhir/us/core/CodeSystem/us-core-documentreference-category"
        ],
    },
    "Encounter": {
        "cat_field": "type",
        "cat_systems": ["http://www.ama-assn.org/go/cpt", "http://snomed.info/sct"],
    },
    "MedicationRequest": {
        "cat_field": "category",
        "cat_systems": ["http://terminology.hl7.org/CodeSystem/medicationrequest-category"],
    },
    "Observation": {
        "cat_field": "category",
        "cat_systems": ["http://terminology.hl7.org/CodeSystem/observation-category"],
    },
}

# Date fields in preference order.
# This prefers "interaction with health system" dates, then administrative dates like "issued",
# then best effort start dates like onsetDateTime.
# See https://github.com/smart-on-fhir/cumulus-library-data-metrics/issues/16 for more.
DATES = {
    "AllergyIntolerance": ["recordedDate", "onsetDateTime", "onsetPeriod.start"],
    "Condition": ["recordedDate", "onsetDateTime", "onsetPeriod.start"],
    "DocumentReference": ["context.period.start", "date"],
    "DiagnosticReport": ["effectiveDateTime", "effectivePeriod.start", "issued"],
    "Encounter": ["period.start"],
    "Immunization": ["occurrenceDateTime", "recorded"],
    "MedicationRequest": ["authoredOn"],
    "Observation": [
        "effectiveDateTime",
        "effectivePeriod.start",
        "effectiveInstant",
        "issued",
    ],
    "Procedure": ["performedDateTime", "performedPeriod.start"],
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
