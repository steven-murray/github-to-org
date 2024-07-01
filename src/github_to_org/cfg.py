"""Configuration."""

from pathlib import Path

import toml

with Path("~/.ghorg").expanduser().open() as fl:
    config = toml.load(fl)


def get_repo_config() -> dict:
    """Get repository configuration from the main config."""
    repos = config["repos"]
    defaults = {k: v for k, v in repos.items() if not isinstance(v, dict)}
    defaults.update(repos.get("defaults", {}))

    orgs = {k: v for k, v in repos.items() if isinstance(v, dict) and k != "defaults"}

    out_repos = {}
    for orgname, org_settings in orgs.items():
        this_defaults = {
            **defaults,
            **{k: v for k, v in org_settings.items() if not isinstance(v, dict)},
        }
        this_defaults |= org_settings.get("defaults", {})

        org_repos = {
            k: v
            for k, v in org_settings.items()
            if isinstance(v, dict) and k != "defaults"
        }

        for repo, settings in org_repos.items():
            actual_settings = {**this_defaults, **settings}
            out_repos[f"{orgname}/{repo}"] = actual_settings

            if "org-file" not in actual_settings:
                raise ValueError(
                    "org-file must be defined either in defaults or each repo"
                )

            actual_settings["org-file"] = Path(actual_settings["org-file"]).expanduser()

    return out_repos
