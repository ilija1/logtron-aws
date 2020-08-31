import boto3


def discover_context(sts_client=None):
    try:
        sts_client = sts_client if sts_client is not None else boto3.client("sts")
        response = sts_client.get_caller_identity()
        arn = response["Arn"]
        last_part = arn.split(":")[-1]
        parts = last_part.split("/")

        type = parts[0]
        id = parts[1]
        region = sts_client.meta.region_name

        context = {
            "id": id,
            "type": type,
            "region": region,
        }

        if type == "assumed-role" and len(parts) > 2:
            context["session_name"] = parts[2]

        return context
    except Exception as ex:
        print(str(ex))
        return {}
