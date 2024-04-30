"""Routines for scraping GitHub Issues."""
import logging

from github import Github, UnknownObjectException

from .cfg import config, get_repo_config

logger = logging.getLogger(__name__)

if "gh-key" in config["settings"]:
    gh = Github(config["settings"]["gh-key"])
else:
    gh = Github(config["settings"]["gh-user"], config["settings"]["gh-pwd"])

user = gh.get_user(config["settings"]["gh-user"])


def get_filtered_issues(repo_name: str, filters: dict) -> list:
    """Get a list of GitHub issues, filtered by the given filters."""
    try:
        repo = gh.get_repo(repo_name)
    except UnknownObjectException as e:
        raise OSError(f"Repo {repo_name} doesn't exist!") from e

    issues = list(repo.get_issues(**{k: v for k, v in filters.items() if k != "prs"}))

    prs = filters.get("prs", True)
    if not prs:
        issues = [iss for iss in issues if iss.pull_request is None]

    return issues


def get_all_github_issues(repo: list[str], org: list[str]) -> dict:
    """Go to your github and grab a big ol' list of issues."""
    repos = get_repo_config()

    if not repo and not org:
        repo = list(repos.keys())
    elif org and not repo:
        repo = [r for r in repos if r.split("/")[0] in org]
    elif repo and not org:
        repo = [r for r in repos if r.split("/")[1] in repo]
    elif repo and org:
        repo = [r for r in repos if r.split("/")[0] in org or r.split("/")[1] in repo]

    return {
        r: get_filtered_issues(r, repos[r].get("filters", {}))
        for r in repos
        if r in repo
    }
