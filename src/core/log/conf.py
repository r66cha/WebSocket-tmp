"""Logging config module."""

# -- Imports

import logging

# -- Exports

__all__ = ["conf_logging"]

# --

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)3s:%(lineno)-3d %(levelname)-3s - %(message)s"
)

# --


def conf_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt=DATE_FORMAT,
        format=LOG_DEFAULT_FORMAT,
    )
