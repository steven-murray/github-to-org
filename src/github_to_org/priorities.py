from functools import wraps
from github.Issue import Issue
from typing import List

_priority_funcs = {None: lambda issue, **kwargs: None}

def prioritizer(func):

    _priority_funcs[func.__name__] = func

    @wraps(func)
    def func_wrapper(issue, **kwargs):
        return func(issue, **kwargs)

    return func_wrapper


def get_priority(issue: Issue, settings: List[dict]) -> [int, None]:
    priority = None

    for setting in settings:
        func = _priority_funcs[setting['fnc']]
        tmp_priority = func(issue, **{k:v for k,v in setting.items() if k!='fnc'})

        if tmp_priority:
            assert len(tmp_priority) == 1
            tmp_priority = tmp_priority.upper()

        if tmp_priority and (priority is None or tmp_priority < priority):
            priority = tmp_priority

    return priority

@prioritizer
def by_milestone(issue: Issue, milestone_map: dict) -> [None, int]:
    if issue.milestone:
        return milestone_map.get(issue.milestone.title, None)


@prioritizer
def by_label(issue: Issue, label_map: dict) -> [None, int]:
    priority = None

    for label in issue.labels:
        if label.name in label_map and (priority is None or (priority and label_map[label.name] < priority)):
            priority = label_map[label.name]

    return priority

@prioritizer
def by_milestone_label(issue: Issue, milestone_map: dict) -> [None, int]:
    if issue.milestone:
        dct = milestone_map.get(issue.milestone.title, {})

        return by_label(issue, label_map=dct)


@prioritizer
def static(issue: Issue, priority: str):
    assert len(priority) == 1
    return priority