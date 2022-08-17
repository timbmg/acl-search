from pydantic import BaseSettings, Field, SecretStr


class RabbitMQSettings(BaseSettings):
    class Config:
        env_prefix = "RABBITMQ_"

    username: str = Field(..., env="RABBITMQ_DEFAULT_USER")
    password: SecretStr = Field(..., env="RABBITMQ_DEFAULT_PASS")
    host: str
    port: str

    @property
    def connection_string(self):
        return (
            f"amqp://{self.username}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}//"
        )
