from typing import Dict, List
from github import Github
from github.ContentFile import ContentFile

from index.settings import GithubSettings


class GithubClient:
    def __init__(self) -> None:
        self.settings = GithubSettings()
        self.github = Github(self.settings.access_token)

    def _get_repo_dir_files(self, repo: str, dir: str) -> List[ContentFile]:
        """Get contents of a directory in a repository."""

        repo = self.github.get_repo(repo)
        files = repo.get_contents(dir)
        files = [f for f in files if f.type == "file"]

        return files

    def _file_to_dict(self, file: ContentFile, properties: List[str] = None):
        _properties = ["sha", "name", "download_url", "last_modified"]
        if properties:
            _properties = list(set(_properties + properties))
        return {p: getattr(file, p) for p in _properties if hasattr(file, p)}

    def get_all_files_from_repo(
        self, repo: str, dir: str, properties: List = None
    ) -> List[Dict]:
        """Get files from a repository."""

        files = self._get_repo_dir_files(repo, dir)
        files = [self._file_to_dict(f, properties) for f in files]

        return files

    def get_file_from_repo(
        self, repo: str, dir: str, filename: str, properties: List[str] = None
    ) -> Dict:
        """Get a file from a repository."""

        files = self._get_repo_dir_files(repo, dir)
        files = [f for f in files if f.name == filename]
        if files:
            assert len(files) == 1, files
            return self._file_to_dict(files[0], properties)
