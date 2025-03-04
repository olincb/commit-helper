__all__ = ["Config"]
import pydantic_settings


class _Config(pydantic_settings.BaseSettings, env_prefix="CO_MIT_"):
    quiet: bool = False


Config = _Config()
