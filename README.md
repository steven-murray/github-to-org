# github-to-org

**Make all your GitHub todo's org-todos.**

I love Emacs org-mode for keeping track of my task lists.
But as a scientist/developer, many of my tasks are encoded as Github issues and PRs. I
don't want to duplicate effort by manually copying each of these into my org files.
This little python package makes it easy to grab all of my Github issues and PRs, and
convert them to org mode format.

## Features:

* Highly configurable. A TOML config file ``~/.ghorg`` houses a very flexible set of
  configurations (like, how to set priorities and schedules for different issues on a
  per-repo basis, or how to filter out certain issues/PRs).
* Extendable. Functions for assigning priorities and schedules are pluggable, so you
  can write your own.
* Only does one-way sync (i.e. it only grabs Github issues, it never updates Github
  from the contents of your org file).
* Does *not* auto-update your org file. It just prints what *you* should add to the
  terminal. So you can always check before giving the OK. We don't like destroying the
  countless hours of work that go into creating our org files, do we?
* Looks at a given org file (set in the config) to see what issues already exist in the
  file, and doesn't print those out.
* Simple CLI interface. Just ``gh2org write`` to print out all your issues in org format.
  Optionally pass ``-r`` to restrict to certain repos, or ``-o`` to restrict to certain
  organizations.


## Setup

To install, simply do::

    pip install git+git://github.com/steven-murray/github-to-org

You'll need to define ``~/.ghorg`` before using it. An example file is included as
``example_ghorg.toml`` in this repo.
