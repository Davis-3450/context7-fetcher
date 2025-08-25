from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

# ---------- enums ----------


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


# ---------- models ----------


class Settings(BaseModel):
    # accept unknown keys & allow aliases
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    # always present
    project: str

    # often missing in compact results → Optional
    title: Optional[str] = None
    description: Optional[str] = None
    branch: Optional[str] = None

    docs_repo_url: Optional[str] = Field(None, alias="docsRepoUrl")
    docs_site_url: Optional[str] = Field(None, alias="docsSiteUrl")

    stars: Optional[int] = None
    trust_score: Optional[float] = Field(None, alias="trustScore")
    vip: Optional[bool] = None
    source_type: Optional[SourceType] = Field(None, alias="type")
    private_repo: Optional[bool] = Field(None, alias="privateRepo")


class Version(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    state: Optional[RunState] = None
    last_update_date: Optional[datetime] = Field(None, alias="lastUpdateDate")
    last_run_state: Optional[RunState] = Field(None, alias="lastRunState")
    last_run_date: Optional[datetime] = Field(None, alias="lastRunDate")
    sha: str = ""

    total_tokens: Optional[int] = Field(None, alias="totalTokens")
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_snippets: Optional[int] = Field(None, alias="totalSnippets")
    total_qa_count: Optional[int] = Field(None, alias="totalQACount")
    parse_failures: Optional[int] = Field(None, alias="parseFailures")
    imported_snippets: Optional[int] = Field(None, alias="importedSnippets")
    average_tokens: Optional[float] = Field(None, alias="averageTokens")
    parse_duration: Optional[int] = Field(None, alias="parseDuration")


class ProjectRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    settings: Settings
    version: Optional[Version] = None
    issues: Dict[str, Any] = Field(default_factory=dict)


class SearchResults(BaseModel):
    model_config = ConfigDict(extra="ignore")
    results: List[ProjectRecord]

    # Allow both {"results": [...]} and bare list responses
    @model_validator(mode="before")
    @classmethod
    def _wrap_list(cls, v):
        if isinstance(v, list):
            return {"results": v}
        return v
