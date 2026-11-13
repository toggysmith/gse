from pathlib import Path

from git import git


class Submodule:
    project: str
    repo: str
    absolute_path: Path
    relative_path: Path
    url: str
    submodules: list[Submodule]

    def __init__(self, project: str, repo: str, absolute_path: Path, relative_path: Path, url: str):
        self.project = project
        self.repo = repo
        self.absolute_path = absolute_path
        self.relative_path = relative_path
        self.url = url

def get_repo_name_from_url(url: str) -> (str, str):
    url = url.split("/")[-2:]
    if len(url[1]) > 4 and url[1][-4:] == ".git":
        url[1] = url[1][:-4]
    return (url[0], url[1])

def get_submodules(path: Path) -> list[Submodule]:
    paths = git(path, ["submodule", "--quiet", "foreach", "--recursive", "pwd"])
    urls = git(path, ["submodule", "--quiet", "foreach", "--recursive", "git", "remote", "get-url", "origin"])

    paths = paths.decode().splitlines()
    urls = urls.decode().splitlines()

    info = [(path, url) for path, url in zip(paths, urls)]

    submodules = []

    for (submodule_path, url) in info:
        submodules.append(Submodule(
            project = get_repo_name_from_url(url)[0],
            repo = get_repo_name_from_url(url)[1],
            absolute_path = submodule_path,
            relative_path = submodule_path[len(str(path)):],
            url = url
        ))

    return submodules
