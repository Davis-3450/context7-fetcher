from enum import Enum


class SourceType(Enum):
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

