import click
from .org import get_org_nodes
from .github import get_all_github_issues
from rich.console import Console
from rich.rule import Rule
from rich.logging import RichHandler
import logging
import toml
from .cfg import get_repo_config, config as CONFIG

console = Console()

main = click.Group()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            # console=console,
            show_time=False,
            show_path=False,
            markup=True,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
        )
    ],
)

@main.command()
@click.option('-r', '--repo', type=str, multiple=True, help='repo(s) to search for')
@click.option('-o', '--org', type=str, multiple=True, help='org(s) to search for')
def write(repo, org):
    issues = get_all_github_issues(repo, org)
    output = get_org_nodes(issues)

    for repo, text in output.items():
        console.rule(repo)
        if text:
            print(text)
        else:
            console.print("[green bold] :heavy_check_mark: All tasks already in org!")
        print()

@main.group()
def config():
    pass

@config.command()
def view():
    console.print(toml.dumps(CONFIG))

@config.command()
def repos():
    console.print(toml.dumps(get_repo_config()))