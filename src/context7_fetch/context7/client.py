from requests import Session

from .models import ProjectRecord, SearchResults


class Client:
    BASE_URL = "https://context7.com"
    # Note: api doesnt need auth, endpoint is public

    def __init__(self):
        self.base_url = self.BASE_URL
        self.session = Session()

    def _get(self, path: str, **kwargs):
        r = self.session.get(self.base_url + path, **kwargs)
        return r

    def search(self, query: str) -> SearchResults:
        data = self._get("/api/search", params={"query": query}).json()
        if isinstance(data, dict) and "results" in data:
            return SearchResults.model_validate(data)
        if isinstance(data, list):
            return SearchResults(
                results=[ProjectRecord.model_validate(x) for x in data]
            )
        raise ValueError("Unexpected /api/search response")

    def fetch_docs(self, project_page: str, limit=100_000):
        # query is optional, 100k forces max.
        # pages are different for website|repo, eg:
        # - https://context7.com/websites/nextjs/llms.txt?tokens=100000
        # - https://context7.com/enginehub/worldedit/llms.txt
        txt_url = project_page + "/llms.txt"
        r = self.session.get(txt_url, params={"tokens": limit})
        return r.text
