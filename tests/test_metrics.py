"""Base class support for unit tests"""

import glob
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import ddt
import duckdb
from cumulus_library import cli


@ddt.ddt
class MetricsTestCase(unittest.TestCase):
    """Test case for data metrics"""

    def test_meta(self):
        self.run_study("meta")

    def test_c_pt_count(self):
        self.run_study("c_pt_count", prefix="count_")

    def test_c_pt_count_no_ext(self):
        self.run_study("c_pt_count", test="no-ext", prefix="count_")

    def test_cubed_output_mode(self):
        # Test directly asking for cube mode via env var
        with mock.patch.dict(os.environ, {"DATA_METRICS_OUTPUT_MODE": "cube"}):
            self.run_study("c_pt_count", test="cubed", prefix="count_", output=None)

        # Test directly asking for cube mode via CLI option
        self.run_study("c_pt_count", test="cubed", prefix="count_", output="cube")

        # Now do the same test but with a bogus arg, confirm it falls back to cube
        self.run_study("c_pt_count", test="cubed", prefix="count_", output="bogus")

        # Now do the same test but without any input, to confirm the default is cube
        self.run_study("c_pt_count", test="cubed", prefix="count_", output=None)

    def test_c_pt_deceased_count(self):
        self.run_study("c_pt_deceased_count", prefix="count_")

    def test_c_resource_count(self):
        self.run_study("c_resource_count", prefix="count_")

    def test_c_resources_per_pt(self):
        self.run_study("c_resources_per_pt")

    def test_c_system_use(self):
        self.run_study("c_system_use", prefix="count_")

    def test_c_us_core_v4_count(self):
        # Just spot checks one resource - the main logic is tested in t_us_core_v4
        self.run_study("c_us_core_v4_count", prefix="count_")

    def test_c_us_core_v4_count_cubed(self):
        # We have special support for cutting up observation profiles into multiple
        # tables in cube mode.
        self.run_study("c_us_core_v4_count", test="cubed", prefix="count_", output="cube")

    def test_q_date_recent(self):
        self.run_study("q_date_recent")

    def test_q_ref_target_pop(self):
        self.run_study("q_ref_target_pop")

    def test_q_ref_target_valid(self):
        self.run_study("q_ref_target_valid")

    def test_q_system_use(self):
        self.run_study("q_system_use")

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

    def run_study(
        self, metric: str, test: str = "general", prefix: str = "", output="aggregate"
    ) -> None:
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
        expected_tables = {name: f"data_metrics__{prefix}{metric}{name}" for name in expected_names}

        # Set up and run the study!
        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy all our study code to this tmpdir
            shutil.copytree(
                f"{root_dir}/cumulus_library_data_metrics",
                f"{tmpdir}/cumulus_library_data_metrics",
            )

            # Because we reload the data-metrics study from different paths each time,
            # python might be keeping the stale imports from previous test builders around.
            # Manually drop em here.
            stale_modules = [
                mod for mod in sys.modules if mod.startswith("cumulus_library_data_metrics")
            ]
            for mod in stale_modules:
                del sys.modules[mod]

            # But change the manifest to only run one test metric, for speed reasons
            manifest_file = f"{tmpdir}/cumulus_library_data_metrics/manifest.toml"
            with open(manifest_file, "w", encoding="utf8") as f:
                f.write(
                    f"""
study_prefix = "data_metrics"
[table_builder_config]
file_names = [
    "{metric}/{metric}.py",
]
                    """
                )

            args = [
                "build",
                # "--verbose",
                "--target=data_metrics",
                f"--study-dir={tmpdir}/cumulus_library_data_metrics",
                "--db-type=duckdb",
                f"--database={tmpdir}/duck.db",
                f"--load-ndjson-dir={data_dir}",
            ]
            if output:
                args.append(f"--option=output-mode:{output}")
            cli.main(args)
            db = duckdb.connect(f"{tmpdir}/duck.db")

            # Uncomment this for extra debugging
            # df = db.execute("select * from data_metrics__xxx").df()
            # print(df.to_string())

            # Check each output with the saved & expected version
            for short_name, full_name in expected_tables.items():
                csv_path = f"{tmpdir}/{full_name}.csv"
                db_table = db.table(full_name)
                sorted_table = db_table.order("ALL DESC NULLS FIRST")
                sorted_table.to_csv(csv_path)
                with open(csv_path, encoding="utf8") as f:
                    csv = f.read()

                expected_path = f"{data_dir}/expected{short_name}.csv"
                with open(expected_path, encoding="utf8") as f:
                    expected_lines = f.readlines()
                    # To allow for comments in expected files, strip them out here
                    expected = "".join(line for line in expected_lines if not line.startswith("#"))

                explanation = f"{short_name}:\n{csv}"
                self.assertEqual(expected, csv, explanation)
