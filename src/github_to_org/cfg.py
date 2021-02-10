import toml
from pathlib import Path

with open(Path('~/.ghorg').expanduser(), 'r') as fl:
    config = toml.load(fl)

def get_repo_config() -> dict:
    repos = config['repos']
    defaults = {k:v for k, v in repos.items() if not isinstance(v, dict)}
    defaults.update(repos.get("defaults", {}))

    orgs = {k: v for k, v in repos.items() if isinstance(v, dict) and k != 'defaults'}

    out_repos = {}
    for orgname, org_settings in orgs.items():
        this_defaults = {
            **defaults,
            **{k:v for k, v in org_settings.items() if not isinstance(v, dict)}
        }
        this_defaults.update(org_settings.get("defaults", {}))

        org_repos = {k:v for k, v in org_settings.items() if isinstance(v, dict) and k != 'defaults'}

        for repo, settings in org_repos.items():
            actual_settings = {
                **this_defaults,
                **settings
            }
            out_repos[f"{orgname}/{repo}"] = actual_settings

    return out_repos
