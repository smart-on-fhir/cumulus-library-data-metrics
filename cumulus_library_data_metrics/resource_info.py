"""Holds various static info about resources we want to examine."""

from cumulus_library_data_metrics import systems

# Categories to slice on
CATEGORIES = {
    "AllergyIntolerance": {
        "cat_field": "category",
    },
    "Condition": {
        "cat_field": "category",
        "cat_systems": [systems.CONDITION_CATEGORY],
    },
    "DiagnosticReport": {
        "cat_field": "category",
        "cat_systems": [systems.LOINC, systems.DIAGNOSTIC_SECTION],
    },
    "DocumentReference": {
        "cat_field": "category",
        "cat_systems": [systems.USCORE_DOCREF_CATEGORY],
    },
    "Encounter": {
        "cat_field": "type",
        "cat_systems": [systems.CPT, systems.SNOMED],
    },
    "MedicationRequest": {
        "cat_field": "category",
        "cat_systems": [systems.MEDREQ_CATEGORY],
    },
    "Observation": {
        "cat_field": "category",
        "cat_systems": [systems.OBSERVATION_CATEGORY],
    },
}

# Date fields in preference order.
# This prefers "interaction with health system" dates, then administrative dates like "issued",
# then best effort start dates like onsetDateTime.
# See https://github.com/smart-on-fhir/cumulus-library-data-metrics/issues/16 for more.
DATES = {
    "AllergyIntolerance": ["recordedDate", "onsetDateTime", "onsetPeriod.start"],
    "Condition": ["recordedDate", "onsetDateTime", "onsetPeriod.start"],
    "DiagnosticReport": ["effectiveDateTime", "effectivePeriod.start", "issued"],
    "DocumentReference": ["context.period.start", "date"],
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
