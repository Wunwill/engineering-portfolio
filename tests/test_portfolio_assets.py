from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class PortfolioAssetTests(unittest.TestCase):
    def test_robot_assets_are_not_published(self):
        for path in (
            "assets/cad/12lb-combat-robot-assembly.step",
            "assets/cad/EXPORT.md",
            "assets/images/combat-robot-assembly.png",
        ):
            with self.subTest(path=path):
                self.assertFalse((ROOT / path).exists())

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
