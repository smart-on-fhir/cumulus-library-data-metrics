"""Module for generating c_resource_count tables"""

import os.path

import jinja2

from cumulus_library.base_table_builder import BaseTableBuilder
from data_metrics.base import MetricMixin


class ResourceCountBuilder(MetricMixin, BaseTableBuilder):
    name = "c_resource_count"

    def make_tables(self, **kwargs) -> None:
        """Make metric tables"""
        if kwargs["src"] in self.DATE_FIELDS:
            self.queries.append(self.render_sql(self.name, period="month", **kwargs))
            self.queries.append(self.render_sql(self.name, period="year", **kwargs))
        else:
            # no date fields, so don't do separate periods
            self.queries.append(self.render_sql(self.name, period="all", **kwargs))

    def prepare_queries(self, *args, **kwargs) -> None:
        # https://github.com/sync-for-science/qualifier/blob/master/metrics.md#c_resource_count-volume-count-of-unique-resources-by-resource-type-by-category-by-year-by-month
        self.make_tables(
            src="AllergyIntolerance",
            category="category",
        )
        self.make_tables(
            src="Condition",
            category="category",
            systems=["http://terminology.hl7.org/CodeSystem/condition-category"],
        )
        self.make_tables(
            src="Device",
        )
        self.make_tables(
            src="DiagnosticReport",
            category="category",
            systems=["http://terminology.hl7.org/CodeSystem/v2-0074"],
        )
        self.make_tables(
            src="DocumentReference",
            category="category",
            systems=["http://hl7.org/fhir/us/core/CodeSystem/us-core-documentreference-category"],
        )
        self.make_tables(
            src="Encounter",
            category="type",
            systems=["http://www.ama-assn.org/go/cpt", "http://snomed.info/sct"],
        )
        self.make_tables(
            src="Immunization",
        )
        self.make_tables(
            src="Medication",
        )
        self.make_tables(
            src="MedicationRequest",
            category="category",
            systems=["http://terminology.hl7.org/CodeSystem/medicationrequest-category"],
        )
        self.make_tables(
            src="Observation",
            category="category",
            systems=["http://terminology.hl7.org/CodeSystem/observation-category"],
        )
        self.make_tables(
            src="Patient",
        )
        self.make_tables(
            src="Procedure",
        )
