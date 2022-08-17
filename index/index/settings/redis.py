from pydantic import BaseSettings, Field, SecretStr


class RedisSettings(BaseSettings):
    class Config:
        env_prefix = "REDIS_"

    username: str = "default"
    password: SecretStr = Field(env="REDIS_PASSWORD")
    host: str
    port: str

    @property
    def connection_string(self):
        return (
            f"redis://{self.username}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}"
        )
