from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SourceType(str, Enum):
    """
    The type of source that the project is from. 'type' in the API response.
    """

    REPO = "repo"
    WEBSITE = "website"
    # ...


class RunState(str, Enum):
    FINALIZED = "finalized"
    INITIAL = "initial"
    ERROR = "error"
