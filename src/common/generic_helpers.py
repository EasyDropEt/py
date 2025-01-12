import uuid

from dotenv import load_dotenv

from src.common.typing.config import Config


def get_new_id() -> uuid.UUID:
    return uuid.uuid4()


def get_config() -> Config:
    load_dotenv()

    return {}
