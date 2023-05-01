from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "event-ticket-system"
    API_V1_STR: str = "/api/v1"

settings = Settings()