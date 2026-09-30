"""Console logging setup for entry points and notebooks."""

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure root logging once; preserve handlers installed by the host."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
