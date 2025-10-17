from pydantic_settings import BaseSettings, SettingsConfigDict

from .utils.rootdir import ROOTDIR


class EnvConfig(BaseSettings):
    postgres_user: str = str(...)
    postgres_password: str = str(...)
    postgres_host: str = str(...)
    postgres_port: int = 5432
    postgres_db: str = str(...)

    model_config = SettingsConfigDict(
        env_file=str(ROOTDIR / ".env"), env_file_encoding="utf-8", case_sensitive=False
    )


env_config = EnvConfig()

if __name__ == "__main__":
    pass
