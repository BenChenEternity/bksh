from datetime import datetime

import UUID.uuid
from stuhelper_app.models import file_share


def create(title, content, file_link, user):  # 发送文件共享
    file_share_object = file_share(id=UUID.uuid.generate(), title=title, content=content, file_link=file_link,
                                   user=user, time=datetime.now().time())
    file_share_object.save()


def delete(id):
    try:
        file_share_object = file_share.objects.get(id=id)
        file_share_object.delete()
    except file_share.DoesNotExist:
        # 处理记录不存在的情况
        pass


def get(id):
    try:
        file_share_object = file_share.objects.get(id=id)
        return file_share_object
    except file_share.DoesNotExist:
        return None  # 如果记录不存在，返回 None


def update(id, new_title, new_content, new_file_link):
    try:
        file_share_object = file_share.objects.get(id=id)
        file_share_object.title = new_title
        file_share_object.content = new_content
        file_share_object.file_link = new_file_link
        file_share_object.save()
    except file_share.DoesNotExist:
        # 处理记录不存在的情况
        pass
