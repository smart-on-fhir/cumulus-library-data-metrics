"""Base class support for unit tests"""

import glob
import os
import shutil
import tempfile
import unittest

import ddt
import duckdb

from cumulus_library import cli


@ddt.ddt
class MetricsTestCase(unittest.TestCase):
    """Test case for quality metrics"""

    def test_c_pt_count(self):
        self.run_study("c_pt_count", prefix="count_")

    def test_c_pt_count_no_ext(self):
        self.run_study("c_pt_count", test="no-ext", prefix="count_")

    def test_c_pt_deceased_count(self):
        self.run_study("c_pt_deceased_count", prefix="count_")

    def test_c_resource_count(self):
        self.run_study("c_resource_count", prefix="count_")

    def test_c_resources_per_pt(self):
        self.run_study("c_resources_per_pt")

    def test_c_term_coverage(self):
        self.run_study("c_term_coverage", prefix="count_")

    def test_c_us_core_v4_count(self):
        # Just spot checks one resource - the main logic is tested in t_us_core_v4
        self.run_study("c_us_core_v4_count", prefix="count_")

    def test_q_ref_target_pop(self):
        self.run_study("q_ref_target_pop")

    def test_q_ref_target_valid(self):
        self.run_study("q_ref_target_valid")

    def test_q_term_use(self):
        self.run_study("q_term_use")

    def test_q_valid_us_core_v4(self):
        # Just spot checks one resource & the summary - the main logic is tested in t_us_core_v4
        self.run_study("q_valid_us_core_v4")

    @ddt.data(
        "mandatory",
        "must-support",
        "allergy-low-schema",
        "docref-low-schema",
        "encounter-low-schema",
        "obs-low-schema",
        "patient-low-schema",
    )
    def test_t_us_core_v4(self, test_name):
        """This is a fake metric, designed just to test profile validity detection"""
        self.run_study("t_us_core_v4", test=test_name)


    # **********************************
    # ** Support code below this line **
    # **********************************


    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def run_study(self, metric: str, test: str = "general", prefix: str = "") -> None:
        """Runs a single test case"""
        test_dir = os.path.dirname(__file__)
        root_dir = os.path.dirname(test_dir)
        data_dir = f"{test_dir}/data/{metric}/{test}"

        # OK which tables are we going to compare in this test?
        expected_result_paths = sorted(glob.glob(f"{data_dir}/expected*.csv"))
        expected_names = [
            path.removeprefix(f"{data_dir}/expected").removesuffix(".csv")
            for path in expected_result_paths
        ]
        expected_tables = {name: f"quality__{prefix}{metric}{name}" for name in expected_names}
        export_tables = '","'.join(expected_tables.values())

        # Set up and run the study!
        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy all our study code to this tmpdir
            shutil.copytree(f"{root_dir}/quality", f"{tmpdir}/quality")

            # But change the manifest to only run one test metric, for speed reasons
            with open(f"{tmpdir}/quality/manifest.toml", "w", encoding="utf8") as f:
                file_config = f"""
[table_builder_config]
file_names = [
    "{metric}/{metric}.py",
]
"""
                f.write(
                    f"""
study_prefix = "quality"

{file_config}

[export_config]
export_list = [
    "{export_tables}",
]
                    """
                )

            cli.main(
                [
                    "build",
                    # "--verbose",
                    "--target=quality",
                    f"--study-dir={tmpdir}/quality",
                    "--db-type=duckdb",
                    f"--database={tmpdir}/duck.db",
                    f"--load-ndjson-dir={data_dir}",
                ]
            )
            db = duckdb.connect(f"{tmpdir}/duck.db")

            # Uncomment this for extra debugging
            # df = db.execute("select * from quality__count_c_term_coverage_allergyintolerance_code_text_counts").df()
            # print(df.to_string())

            # Check each output with the saved & expected version
            for short_name, full_name in expected_tables.items():
                csv_path = f"{tmpdir}/{full_name}.csv"
                db_table = db.table(full_name)
                sorted_table = db_table.order(f"ALL DESC NULLS FIRST")
                sorted_table.to_csv(csv_path)
                with open(csv_path, "r", encoding="utf8") as f:
                    csv = f.read()

                expected_path = f"{data_dir}/expected{short_name}.csv"
                with open(expected_path, "r", encoding="utf8") as f:
                    expected_lines = f.readlines()
                    # To allow for comments in expected files, strip them out here
                    expected = ''.join(line for line in expected_lines if not line.startswith("#"))

                explanation = f"{short_name}:\n{csv}"
                self.assertEqual(expected, csv, explanation)
