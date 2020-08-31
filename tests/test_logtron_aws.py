from logtron_aws import CloudWatchHandler
from logtron_aws import discover_context


def test_cloudwatch():
    pass


def test_context():
    class MockClientMeta:
        def __init__(self):
            self.region_name = "us-east-1"

    class MockClient:
        def __init__(self):
            self.meta = MockClientMeta()

        def get_caller_identity(self):
            return {"Arn": "arn:aws:sts::123456789012:assumed-role/foo/session1"}

    context = discover_context(sts_client=MockClient())
    assert context["id"] is not None
