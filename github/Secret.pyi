import datetime
from typing import List, Any, Dict
from github.GithubObject import CompletableGithubObject
from github.Repository import Repository

class Secret(CompletableGithubObject):
    def __repr__(self) -> str: ...
    def _initAttributes(self) -> None: ...
    def _useAttributes(self, attributes: Dict[str, Any]) -> None: ...
    def delete(self) -> None: ...
    def add_repo(self, repo: Repository) -> bool: ...
    def remove_repo(self, repo: Repository) -> bool: ...
    def _refresh_repos(self) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def created_at(self) -> datetime.datetime: ...
    @property
    def updated_at(self) -> datetime.datetime: ...
    @property
    def visibility(self) -> str: ...
    @property
    def selected_repositories(self) -> List[Repository]: ...
    @property
    def url(self) -> str: ...
