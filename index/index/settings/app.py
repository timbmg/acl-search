from pydantic import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        env_prefix = "INDEX_"
