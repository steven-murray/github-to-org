"""Methods for creating an Org structure/file"""
import datetime as dt
import logging
import warnings
from github.Issue import Issue
from pathlib import Path
from typing import List, Tuple

from .cfg import get_repo_config
from .priorities import get_priority
from .schedules import get_schedule

logger = logging.getLogger(__name__)


def get_node_level(line) -> int:
    """Get the node level of a line, returning 0 if the line doesn't define a node."""
    if line.strip().startswith("*"):
        return len(line.strip().split(" ")[0])
    else:
        return 0


def get_org_node(repo_name: str, fname: [str, Path]) -> Tuple[str, int]:
    """Get a unique org node associated with a repository"""

    with open(fname, "r") as fl:
        in_node = False
        n_lines = 0
        lines = fl.readlines()
        start = None
        for i, line in enumerate(lines):
            node_level = get_node_level(line)
            if (
                node_level
                and " " + repo_name.split("/")[1].lower() in line.lower()
                and ":gh:" in line
            ):
                in_node = True
                start = i
                level = node_level  # Number of *'s at the beginning of the line
                continue

            if in_node:
                n_lines += 1
                if get_node_level(line) == level:
                    break

        if start is not None:
            out = "".join(lines[start : start + n_lines])
            return out, level
        else:
            return None, None


def get_existing_tasks(node: str, repo: str) -> List[int]:
    """Find issue/pr ids of tasks already in the task list."""
    ids = []
    for line in node.split("\n"):
        if f"{repo.lower()}/issues/" in line.lower():
            logger.debug(f"Found /issues/ in line {line}")
            try:
                ids.append(int(line.split("/issues/")[-1].split("]")[0]))
            except ValueError:
                warnings.warn(
                    f"This line has formatting incompatible with gh2org: {line}"
                )
        elif f"{repo.lower()}/pulls/" in line.lower():
            logger.debug(f"Found /pull/ in line {line}")
            try:
                ids.append(int(line.split("/pull/")[-1].split("]")[0]))
            except ValueError:
                warnings.warn(
                    f"This line has formatting incompatible with gh2org: {line}"
                )
    return ids


def convert_issue_list_to_org(
    issues: List[Issue], existing_tasks: List[int], settings: dict, level: int
) -> str:
    """Convert your list of issues to an Org structure"""
    text = ""
    for issue in issues:
        if issue.number not in existing_tasks:
            priority = get_priority(issue, settings.get("priority", []))
            schedule = get_schedule(issue, settings.get("schedule", {}))
            text += issue_to_node_str(issue, priority, schedule, level + 1)

    return text


def issue_to_node_str(
    issue: Issue, priority: [None, str], schedule: dt.datetime, level: int
):
    if priority is None:
        priority = ""
    else:
        priority = f"[#{priority}]"

    if schedule is None:
        schedule = ""
    else:
        schedule = f"DEADLINE: <{schedule.year}-{schedule.month}-{schedule.day}>"

    return (
        f"{'*'*level} TODO {priority} [[{issue.html_url}][{issue.repository.name}/"
        f"{issue.number}]]: {issue.title}\n"
    )


def get_org_nodes(issues: dict) -> dict:
    repo_cfg = get_repo_config()

    out = {}
    for repo, issue_list in issues.items():

        node, level = get_org_node(repo, repo_cfg[repo]["org-file"])
        logger.debug(f"For repo {repo}, got node text:")
        logger.debug(node)
        if node is not None:
            existing = get_existing_tasks(node, repo)
        else:
            existing = []

        text = convert_issue_list_to_org(
            issue_list,
            existing_tasks=existing,
            settings=repo_cfg[repo],
            level=level or 0,
        )

        out[repo] = text

    return out


def write_org(org, fname: [str, Path]):
    """Write out an Org structure to file"""
    pass
