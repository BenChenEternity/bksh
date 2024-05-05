import uuid


def generate():
    # 生成一个UUID
    uuid_val = uuid.uuid4()

    # 将UUID转换为字符串，并取前16位字符
    short_uuid = str(uuid_val).replace("-", "")[:16]

    return short_uuid
