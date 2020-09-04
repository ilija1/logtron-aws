class MockSTSClientMeta:
    def __init__(self):
        self.region_name = "us-east-1"


class MockSTSClient:
    def __init__(self):
        self.meta = MockSTSClientMeta()

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

    def get_paginator(self, name):
        return self.paginator

    def create_log_group(self, **kwargs):
        pass

    def create_log_stream(self, **kwargs):
        pass

    def put_log_events(self, **kwargs):
        [print(i) for i in kwargs["logEvents"]]
        return {"nextSequenceToken": "123"}
