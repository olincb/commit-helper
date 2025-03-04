__all__ = ["Config"]
import pydantic_settings


class _Config(pydantic_settings.BaseSettings, env_prefix="CO_MIT_"):
    example: str | None = None
    openai_api_key: str | None = None
    quiet: bool = False


Config = _Config()
