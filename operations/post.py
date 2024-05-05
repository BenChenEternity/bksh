from datetime import datetime

import UUID.uuid
from stuhelper_app.models import Post


def create_post(title, content, category, user):  # 发送动态
    post_object = Post(id=UUID.uuid.generate(), title=title, content=content, category=category, user=user,
                       time=datetime.now().time())
    post_object.save()


def delete_post(post_id):  # 删除动态
    try:
        post_object = Post.objects.get(id=post_id)
        post_object.delete()
    except Post.DoesNotExist:
        # 处理记录不存在的情况
        pass


def get_post(post_id):
    try:
        post_object = Post.objects.get(id=post_id)
        return post_object
    except Post.DoesNotExist:
        return None  # 如果记录不存在，返回 None


def update_post(post_to_update, new_title, new_content, new_post_type):
    try:
        post_object = Post.objects.get(id=post_to_update)
        post_object.title = new_title
        post_object.content = new_content
        post_object.post_type = new_post_type
        post_object.save()
    except Post.DoesNotExist:
        # 处理记录不存在的情况
        pass
