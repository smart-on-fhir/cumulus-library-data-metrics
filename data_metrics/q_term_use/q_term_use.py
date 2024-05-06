"""Module for generating q_term_use tables"""

import os.path

import jinja2

from cumulus_library.base_table_builder import BaseTableBuilder
from data_metrics.base import MetricMixin


class TermUseBuilder(MetricMixin, BaseTableBuilder):
    name = "q_term_use"

    def make_table(self, **kwargs) -> None:
        """Make a single metric table"""
        summary_key = f"{kwargs['src'].lower()}_{kwargs['field'].lower()}"
        self.summary_entries[summary_key] = None

        self.queries.append(self.render_sql(self.name, **kwargs))

    def add_metric_queries(self) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#q_term_use-conformance-expect-common-terminology-systems-to-be-populated
        # With some differences:
        # - Allow multiple systems (pulled from US Core v4 profile recommendations)
        self.make_table(src="AllergyIntolerance", field="code", systems=[
            "http://snomed.info/sct",
            "http://www.nlm.nih.gov/research/umls/rxnorm",
        ]),
        self.make_table(src="Condition", field="code", systems=[
            "http://hl7.org/fhir/sid/icd-10-cm",
            "http://hl7.org/fhir/sid/icd-9-cm",
            "http://snomed.info/sct",
        ]),
        self.make_table(src="Device", field="type", systems=["http://snomed.info/sct"]),
        self.make_table(src="DiagnosticReport", field="code", systems=["http://loinc.org"]),
        self.make_table(src="DocumentReference", field="type", systems=["http://loinc.org"]),
        self.make_table(src="Immunization", field="vaccineCode", systems=[
            # The FHIR spec also gives urn:oid:1.2.36.1.2001.1005.17 as an example, but the US Core
            # profile drops that suggestion in favor of only CVX.
            "http://hl7.org/fhir/sid/cvx",
        ]),
        self.make_table(src="Medication", field="code", systems=[
            # The FHIR spec gives SNOMED as an example, but the US Core profile drops that
            # suggestion in favor of only RxNorm
            "http://www.nlm.nih.gov/research/umls/rxnorm",
        ]),
        self.make_table(src="MedicationRequest", field="medicationCodeableConcept", systems=[
            # The FHIR spec gives SNOMED as an example, but the US Core profile drops that
            # suggestion in favor of only RxNorm
            "http://www.nlm.nih.gov/research/umls/rxnorm",
        ]),
        self.make_table(src="Observation", field="code", systems=["http://loinc.org"]),
        self.make_table(src="Observation", field="valueCodeableConcept", systems=[
            # Base FHIR doesn't suggest anything specific here, but the Laboratory and
            # Smoking Status profiles both want SNOMED.
            "http://snomed.info/sct",
        ]),
        self.make_table(src="Procedure", field="code", systems=[
            # Base FHIR only gives SNOMED as an example. But the US Core v4 profile lists all these.
            "http://loinc.org",
            "http://snomed.info/sct",
            "http://www.ada.org/cdt",
            "http://www.ama-assn.org/go/cpt",
            "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
            "http://www.cms.gov/Medicare/Coding/ICD10",
        ]),
        self.make_summary()
