class MockSTSClientMeta:
    def __init__(self):
        self.region_name = "us-east-1"


class MockSTSClient:
    def __init__(self):
        self.meta = MockSTSClientMeta()

    def get_caller_identity(self):
        return {"Arn": "arn:aws:sts::123456789012:assumed-role/foo/session1"}


class MockLogsPaginator:
    def __init__(self):
        pass

    def paginate(self, **kwargs):
        return []


class MockLogsClient:
    def __init__(self):
        pass

    def get_paginator(self, name):
        return MockLogsPaginator()

    def create_log_group(self, **kwargs):
        pass

    def create_log_stream(self, **kwargs):
        pass

    def put_log_events(self, **kwargs):
        return {"nextSequenceToken": "123"}
