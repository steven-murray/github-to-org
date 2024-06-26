"""CLI interface."""
import logging

import click
import toml
from rich.console import Console
from rich.logging import RichHandler

from .cfg import config as CONFIG  # noqa: N812
from .cfg import get_repo_config
from .github import get_all_github_issues
from .org import get_org_nodes

console = Console()

main = click.Group()

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            console=console,
            show_time=False,
            show_path=False,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
        )
    ],
)


@main.command()
@click.option("-r", "--repo", type=str, multiple=True, help="repo(s) to search for")
@click.option("-o", "--org", type=str, multiple=True, help="org(s) to search for")
@click.option(
    "-l",
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    help="log level",
    default="INFO",
)
def write(repo, org, log_level):
    """Write required tasks to console."""
    logging.getLogger("github_to_org").setLevel(log_level)

    issues = get_all_github_issues(repo, org)
    output, closers = get_org_nodes(issues)
    for repo, text in output.items():
        console.rule(repo)
        if text:
            console.print(text)
        else:
            console.print("[green bold] :heavy_check_mark: All tasks already in org!")

        ctxt = closers[repo]
        if ctxt:
            console.print()
            console.print("[red bold]ISSUES TO CLOSE:")
            console.print(ctxt)

        console.print()


@main.group()
def config():
    """Group of commands to do with configuration."""


@config.command()
def view():
    """View the current configuration."""
    console.print(toml.dumps(CONFIG))


@config.command()
def repos():
    """View the list of repositories configured."""
    console.print(toml.dumps(get_repo_config()))
