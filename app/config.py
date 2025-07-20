from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DATABASE: str

    model_config = SettingsConfigDict(
        env_file='./.env',
        env_ignore_empty=True,
        extra="ignore"
    )

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

settings = DatabaseSettings()


print(settings.POSTGRES_URL)