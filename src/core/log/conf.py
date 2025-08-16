"""Logging config module."""

# -- Imports

import logging

# -- Exports

__all__ = ["conf_logging"]

# --


def conf_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)-8s:%(lineno)-8d %(levelname)-8s - %(message)s",
    )
