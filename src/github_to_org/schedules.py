"""Functions that can set schedules based on issue properties."""
import datetime as dt
from functools import wraps

from github.Issue import Issue

from .github import user

_schedule_funcs = {None: lambda issue, **kwargs: None}


def scheduler(func):
    """Mark a function as a scheduler."""
    _schedule_funcs[func.__name__] = func

    @wraps(func)
    def func_wrapper(issue, **kwargs):
        return func(issue, **kwargs)

    return func_wrapper


def get_schedule(issue: Issue, settings: list[dict]) -> dt.datetime:
    """Get a schedule."""
    schedule = None
    for func_name, setting in settings.items():
        func = _schedule_funcs[func_name]
        tmp_schedule = func(issue, **setting)

        if tmp_schedule and (schedule is None or tmp_schedule < schedule):
            schedule = tmp_schedule

    return schedule


@scheduler
def pr_review(issue: Issue, deadline: int):
    """Set a schedule for PR reviews as a certain number of days."""
    if issue.pull_request is not None:
        pr = issue.as_pull_request()
        rvs = list(pr.get_review_requests()[0])

        if user in rvs:
            return issue.created_at + dt.timedelta(days=deadline)
