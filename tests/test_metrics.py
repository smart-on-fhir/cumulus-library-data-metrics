"""Base class support for unit tests"""

import os
import shutil
import tempfile
import unittest

from cumulus_library import cli


class MetricsTestCase(unittest.TestCase):
    """Test case for quality metrics"""

    def test_q_ref_target_pop(self):
        self.run_study("q_ref_target_pop")

    def test_q_ref_target_valid(self):
        self.run_study("q_ref_target_valid")

    def test_q_term_use(self):
        self.run_study("q_term_use")


    # **********************************
    # ** Support code below this line **
    # **********************************


    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def run_study(self, metric: str, test: str = "general") -> None:
        """Runs a single test case"""
        test_dir = os.path.dirname(__file__)
        root_dir = os.path.dirname(test_dir)
        data_dir = f"{test_dir}/data/{metric}/{test}"
        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy all our study code to this tmpdir
            shutil.copytree(f"{root_dir}/quality", f"{tmpdir}/quality")

            # But change the manifest to only run one test metric, for speed reasons
            with open(f"{tmpdir}/quality/manifest.toml", "w", encoding="utf8") as f:
                f.write(
                    f"""
study_prefix = "quality"

[table_builder_config]
file_names = [
    "{metric}.py",
]

[export_config]
export_list = [
    "quality__{metric}_summary",
]
                    """
                )

            cli.main(
                [
                    "build",
                    "--target=quality",
                    f"--study-dir={tmpdir}/quality",
                    "--db-type=duckdb",
                    f"--database={tmpdir}/duck.db",
                    f"--load-ndjson-dir={data_dir}",
                ]
            )
            cli.main(
                [
                    "export",
                    "--target=quality",
                    f"--study-dir={tmpdir}/quality",
                    "--db-type=duckdb",
                    f"--database={tmpdir}/duck.db",
                    f"{tmpdir}/counts",
                ]
            )

            # Uncomment this for extra debugging
            # import duckdb
            # df = duckdb.connect(f"{tmpdir}/duck.db").execute("SELECT * FROM xxx").df()
            # print(df.to_string())

            csv_path = f"{tmpdir}/counts/quality/quality__{metric}_summary.csv"
            with open(csv_path, "r", encoding="utf8") as f:
                csv = f.read()
            expected_path = f"{data_dir}/expected.csv"
            with open(expected_path, "r", encoding="utf8") as f:
                expected_lines = f.readlines()
                # To allow for comments in expected files, strip them out here
                expected = ''.join(line for line in expected_lines if not line.startswith("#"))
            self.assertEqual(expected, csv)
