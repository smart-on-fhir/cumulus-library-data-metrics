"""Terminology system constants and information."""

CPT = "http://www.ama-assn.org/go/cpt"
CVX = "http://hl7.org/fhir/sid/cvx"
ICD9CM = "http://hl7.org/fhir/sid/icd-9-cm"
ICD10CM = "http://hl7.org/fhir/sid/icd-10-cm"
LOINC = "http://loinc.org"
NDC = "http://hl7.org/fhir/sid/ndc"
NULL_FLAVOR = "http://terminology.hl7.org/CodeSystem/v3-NullFlavor"
RXNORM = "http://www.nlm.nih.gov/research/umls/rxnorm"
SNOMED = "http://snomed.info/sct"
UCUM = "http://unitsofmeasure.org"

# Resource-specific systems
CONDITION_CATEGORY = "http://terminology.hl7.org/CodeSystem/condition-category"
DIAGNOSTIC_SECTION = "http://terminology.hl7.org/CodeSystem/v2-0074"
MEDREQ_CATEGORY = "http://terminology.hl7.org/CodeSystem/medicationrequest-category"
OBSERVATION_CATEGORY = "http://terminology.hl7.org/CodeSystem/observation-category"
USCORE_CONDITION_CATEGORY = "http://hl7.org/fhir/us/core/CodeSystem/condition-category"
USCORE_DOCREF_CATEGORY = "http://hl7.org/fhir/us/core/CodeSystem/us-core-documentreference-category"

# Object Identifiers (OIDs).
# FHIR does not like to see them used (instead the http URL should be used).
# But some EHRs really like OIDs and may use them anyway.
# In terms of data metrics - we do not allow OIDs for any kind of validation
# or quality metrics. But for characterization metrics, we do look for them.
# See:
# https://www.hl7.org/fhir/R4/terminologies.html#system
# https://www.hl7.org/fhir/R4/terminologies-systems.html
OIDS = {
    CPT: "urn:oid:2.16.840.1.113883.6.12",
    CVX: "urn:oid:2.16.840.1.113883.12.292",
    ICD9CM: "urn:oid:2.16.840.1.113883.6.2",
    ICD10CM: "urn:oid:2.16.840.1.113883.6.90",
    LOINC: "urn:oid:2.16.840.1.113883.6.1",
    NDC: "urn:oid:2.16.840.1.113883.6.69",
    RXNORM: "urn:oid:2.16.840.1.113883.6.88",
    SNOMED: "urn:oid:2.16.840.1.113883.6.96",
    UCUM: "urn:oid:2.16.840.1.113883.6.8",
}

NAMES = {
    CPT: "CPT",
    CVX: "CVX",
    ICD9CM: "ICD-9-CM",
    ICD10CM: "ICD-10-CM",
    LOINC: "LOINC",
    NDC: "NDC",
    RXNORM: "RxNorm",
    SNOMED: "SNOMED",
    UCUM: "UCUM",
}
# Add all the OID versions too
for system, oid_system in OIDS.items():
    if system in NAMES:
        NAMES[oid_system] = f"{NAMES[system]} (OID)"
