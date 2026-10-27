import hashlib
from pathlib import Path
import re
import struct
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / "assets/cad/12lb-combat-robot-assembly.step"
CAD_SHA256 = "1f120b062ecf56b7b5781c713e10997b81dd58b24675d2242034b64ceb8e33d8"


class PortfolioAssetTests(unittest.TestCase):
    def test_cad_matches_original_download(self):
        self.assertEqual(CAD.stat().st_size, 11456031)
        self.assertEqual(hashlib.sha256(CAD.read_bytes()).hexdigest(), CAD_SHA256)

    def test_step_file_has_complete_container(self):
        content = CAD.read_bytes()
        self.assertTrue(content.startswith(b"ISO-10303-21;"))
        self.assertTrue(content.rstrip().endswith(b"END-ISO-10303-21;"))

    def test_preview_is_full_size_png(self):
        header = (ROOT / "assets/images/combat-robot-assembly.png").read_bytes()[:24]
        self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", header[16:24])
        self.assertGreaterEqual(width, 1000)
        self.assertGreaterEqual(height, 500)

    def test_relative_markdown_links_resolve_inside_repository(self):
        for document in ROOT.rglob("*.md"):
            targets = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", document.read_text(encoding="utf-8"))
            for target in targets:
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                with self.subTest(document=document.relative_to(ROOT), target=target):
                    destination = (document.parent / unquote(parsed.path)).resolve()
                    self.assertTrue(destination.is_relative_to(ROOT))
                    self.assertTrue(destination.is_file(), f"Missing link target: {destination}")


if __name__ == "__main__":
    unittest.main()
