"""Application configuration module."""

# -- Imports

from pydantic_settings import BaseSettings
from src.core.schemas import DescriptionAppSchema

# -- Exports

__all__ = ["settings"]

# --


class Settings(BaseSettings):
    """Main application settings."""

    _description: DescriptionAppSchema = DescriptionAppSchema()


settings = Settings()
