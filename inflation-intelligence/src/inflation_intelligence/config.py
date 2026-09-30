"""Small, explicit environment configuration; no import-time side effects."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    log_level: str


def load_settings() -> Settings:
    """Read settings from the current process environment without loading .env."""
    level = os.environ.get("INFLATION_LOG_LEVEL", "INFO").strip().upper()
    if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ValueError("INFLATION_LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR, or CRITICAL")
    directory = os.environ.get("INFLATION_DATA_DIR", "data").strip()
    if not directory:
        raise ValueError("INFLATION_DATA_DIR must not be empty")
    return Settings(data_dir=Path(directory).expanduser().resolve(), log_level=level)
