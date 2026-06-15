from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_mayuscula_user: str
    api_mayuscula_pass: str
    api_mayuscula_url: str

    class Config():
        env_file = ".env"
        case_sensitive = False

settings = Settings()