import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from examples.chamber_plot_index import Chamber, build_index, parse_plot_path


ROOT = Path(__file__).resolve().parents[1]


class ChamberPlotIndexTests(unittest.TestCase):
    def test_parse_detector_identifiers(self):
        chamber, path = parse_plot_path("MB-2/1/05/dt_bellcurves.png")
        self.assertEqual(chamber, Chamber(-2, 1, 5))
        self.assertEqual(path, "MB-2/1/05/dt_bellcurves.png")

    def test_normalize_windows_separators(self):
        self.assertEqual(
            parse_plot_path(r"MB+1\3\12\plot.png"),
            (Chamber(1, 3, 12), "MB+1/3/12/plot.png"),
        )

    def test_station_four_extra_sectors(self):
        for sector in (13, 14):
            self.assertEqual(
                parse_plot_path(f"MB-0/4/{sector}/plot.png")[0],
                Chamber(0, 4, sector),
            )

    def test_invalid_chambers(self):
        for identifiers in ((3, 1, 1), (0, 0, 1), (0, 1, 13), (0, 4, 15), (0, 1, 0)):
            with self.subTest(identifiers=identifiers), self.assertRaises(ValueError):
                Chamber(*identifiers)

    def test_reject_unsafe_or_unsupported_paths(self):
        for path in (
            "/MB-2/1/05/a.png", "../MB-2/1/05/a.png", "MB-2/1/05/../a.png",
            "MB-2/1/05/a.root", "MB-2/1/5/a.png", "MB-ALL/1/05/a.png",
            "MB-2//05/a.png", "MB-2/1/05/a.png?token=secret", None, 12,
        ):
            with self.subTest(path=path), self.assertRaises(ValueError):
                parse_plot_path(path)

    def test_lookup_deduplicates_and_stays_with_selected_chamber(self):
        paths = ["MB-2/1/05/b.png", "MB-2/1/06/a.png", "MB-2/1/05/a.png",
                 "MB-2/1/05/b.png"]
        index = build_index(paths)
        self.assertEqual(index[Chamber(-2, 1, 5)],
                         ("MB-2/1/05/a.png", "MB-2/1/05/b.png"))
        self.assertEqual(index.get(Chamber(2, 4, 14), ()), ())
        self.assertEqual(index, build_index(reversed(paths)))

    def test_empty_input(self):
        self.assertEqual(build_index([]), {})

    def test_command_line_example(self):
        result = subprocess.run(
            [sys.executable, "examples/chamber_plot_index.py",
             "examples/synthetic_plot_paths.json", "--wheel", "-2",
             "--station", "1", "--sector", "5"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(result.stdout), [
            "MB-2/1/05/dt_bellcurves.png", "MB-2/1/05/dt_polynomials.png",
        ])

    def test_invalid_manifest_reports_error_without_traceback(self):
        for content in ('{"paths": []}', '[null]', 'not json'):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as folder:
                manifest = Path(folder) / "paths.json"
                manifest.write_text(content, encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, str(ROOT / "examples/chamber_plot_index.py"),
                     str(manifest), "--wheel", "0", "--station", "1", "--sector", "1"],
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
