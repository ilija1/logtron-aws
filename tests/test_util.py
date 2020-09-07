from logtron_aws.util import path_get


def test_path_get():
    d = {"context": {"id": "abcd"}}
    val = path_get(d, "context.id")
    assert val[0] == "abcd"

    val = path_get(d, "bobo.jojo.koko")
    assert val[0] is None

    d = {"context_id": "abcd"}
    val = path_get(d, "context.id")
    assert val[0] == "abcd"
