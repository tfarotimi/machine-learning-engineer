"""Check environment validation without touching user data."""

import unittest
from pathlib import Path
from unittest.mock import patch

from inflation_intelligence.config import load_settings


class SettingsTests(unittest.TestCase):
    @patch.dict("os.environ", {}, clear=True)
    def test_defaults(self):
        settings = load_settings()
        self.assertEqual(settings.log_level, "INFO")
        self.assertEqual(settings.data_dir, Path("data").resolve())

    @patch.dict("os.environ", {"INFLATION_LOG_LEVEL": " debug ", "INFLATION_DATA_DIR": "audit-data"}, clear=True)
    def test_overrides(self):
        settings = load_settings()
        self.assertEqual(settings.log_level, "DEBUG")
        self.assertEqual(settings.data_dir, Path("audit-data").resolve())

    def test_invalid_configuration(self):
        for values in ({"INFLATION_LOG_LEVEL": "INF"}, {"INFLATION_DATA_DIR": " "}):
            with self.subTest(values=values), patch.dict("os.environ", values, clear=True):
                with self.assertRaises(ValueError):
                    load_settings()
