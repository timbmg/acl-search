from pydantic import BaseSettings, Field


class ElasticSearchSettings(BaseSettings):
    class Config:
        env_prefix = "ELASTICSEARCH_"

    host: str
    port: str
    timeout: int = Field(30)
    retry_on_timeout: bool = Field(True)
    max_retries: int = Field(10)

    @property
    def connection_string(self):
        return f"http://{self.host}:{self.port}"
