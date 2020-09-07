from collections import namedtuple


class MockSTSClient:
    def __init__(self):
        self.meta = namedtuple("meta", "region_name")._make(["us-east-1"])

    def get_caller_identity(self):
        return {"Arn": "arn:aws:sts::123456789012:assumed-role/foo/session1"}


class MockLogsPaginator:
    def __init__(self, items=[]):
        self.items = items

    def paginate(self, **kwargs):
        for i in self.items:
            yield i


class MockLogsClient:
    def __init__(self, paginator=None):
        self.paginator = paginator if paginator is not None else MockLogsPaginator()
        self.meta = namedtuple("meta", "events")._make(
            [namedtuple("events", "register_first")._make([lambda _, __: None])]
        )

    def get_paginator(self, name):
        return self.paginator

    def create_log_group(self, **kwargs):
        pass

    def create_log_stream(self, **kwargs):
        pass

    def put_log_events(self, **kwargs):
        for i in kwargs["logEvents"]:
            print(i)
        return {"nextSequenceToken": "123"}
