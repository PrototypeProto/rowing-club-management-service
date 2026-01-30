from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    '''
        Dictates where to get the environment vars and 
            exports the settings to be used throughout the project
    '''
    DB_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


Config = Settings()