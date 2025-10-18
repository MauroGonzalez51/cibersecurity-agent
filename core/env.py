from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from .utils.rootdir import ROOTDIR


class EnvConfig(BaseSettings):
    postgres_user: str = str(...)
    postgres_password: str = str(...)
    postgres_host: str = str(...)
    postgres_port: int = 5432
    postgres_db: str = str(...)

    openrouter_api_key: str = str(...)
    virustotal_api_key: str = str(...)
    geoip_database_path: Path = Path(
        ROOTDIR / "core" / "data" / "GeoLite2-City_20251017" / "GeoLite2-City.mmdb"
    )

    model_config = SettingsConfigDict(
        env_file=str(ROOTDIR / ".env"), env_file_encoding="utf-8", case_sensitive=False
    )


env_config = EnvConfig()

if __name__ == "__main__":
    pass
