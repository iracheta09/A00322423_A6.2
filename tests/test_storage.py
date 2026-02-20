"""Tests for JSON storage helpers."""

import unittest
from pathlib import Path
import tempfile

from src.storage import load_json, save_json


class TestStorage(unittest.TestCase):
    """Unit tests for load_json and save_json behavior."""

    def test_load_missing_file_returns_default(self):
        """Returns provided default when file does not exist."""
        with tempfile.TemporaryDirectory() as d:
            missing = Path(d) / "nope.json"
            self.assertEqual(load_json(missing, default=[]), [])

    def test_save_and_load_roundtrip(self):
        """Saves JSON and loads it back without data loss."""
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "data.json"
            obj = {"a": 1, "b": ["x", "y"]}
            save_json(f, obj)
            self.assertEqual(load_json(f, default={}), obj)

    def test_load_empty_file_returns_default(self):
        """Returns default when file exists but content is empty."""
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "empty.json"
            f.write_text("", encoding="utf-8")
            self.assertEqual(load_json(f, default={"ok": True}), {"ok": True})

    def test_load_invalid_json_returns_default(self):
        """Returns default when file contains invalid JSON."""
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "bad.json"
            f.write_text("{ bad json", encoding="utf-8")
            self.assertEqual(load_json(f, default=123), 123)


if __name__ == "__main__":
    unittest.main()
