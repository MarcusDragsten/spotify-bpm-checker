import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


class Config(BaseSettings):
    CLIENT_ID: str | None = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str | None = os.getenv("CLIENT_SECRET")


config = Config()  # type: ignore[call-arg]
