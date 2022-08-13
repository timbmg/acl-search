from pydantic import BaseSettings


class GithubSettings(BaseSettings):
    class Config:
        env_prefix = "GITHUB_"

    access_token: str
