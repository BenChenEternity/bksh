from time import sleep

from celery.task import task
from django.test import TestCase

# Create your tests here.

# 添加五个新的empty_classroom
from stuhelper_app.models import Empty_Classroom

import json
from stuhelper_app.models import Empty_Classroom, Post, CustomUser
from django.contrib.auth import get_user_model


def create_emptyclassroom_test(filename, campus):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for entry in data:
        week = entry["week"]
        day = entry["day"]
        session = entry["session"]
        results = entry["result"]

        for result in results:
            cdbh = result["cdbh"]
            lh = result["lh"]
            lch = result["lch"]
            if not lch:
                lch = 1
            zws = result["zws"]
            kszws1 = result["kszws1"]

            Empty_Classroom.objects.create(location_id=cdbh, building_id=lh, floor_id=int(lch), seat_num=int(zws),
                                           exam_seat_num=int(kszws1),
                                           classroom_type=1, empty_week=week, empty_day=day, empty_session=int(session),
                                           campus=campus)


def delete_empty_classroom():
    Empty_Classroom.objects.all().delete()


def create_post():
    # Post.objects.create(title='post1', content='This is the content of post1', post_type='二手闲置',
    #                     author=CustomUser.objects.filter(id=6).first())
    # Post.objects.create(title='post2', content='This is the content of post2', post_type='二手闲置',
    #                     author=CustomUser.objects.filter(id=6).first())

    for i in range(1, 20):
        Post.objects.create(title='post' + str(i), content='This is the content of post' + str(i), post_type='二手闲置',
                            author=CustomUser.objects.filter(id=7).first())

    for i in range(20, 40):
        Post.objects.create(title='post' + str(i), content='This is the content of post' + str(i), post_type='打听求助',
                            author=CustomUser.objects.filter(id=7).first())


def clear_post():
    Post.objects.all().delete()


def test():
    empty_classrooms = Empty_Classroom.objects.filter(
        empty_week='1', empty_day='1', campus=str(2),
        empty_session__gte='1', empty_session__lte='2')
    print(empty_classrooms)


def changeto_breif_content():
    posts = Post.objects.all()
    for post in posts:
        post.brief_content = post.content[:20] + '  ...'
        post.save()


def create_motoo():
    users = CustomUser.objects.all()
    for user in users:
        user.motto = '这个人很懒，什么都没有留下'
        user.save()


def test_user(user_id):
    User = get_user_model()
    print(User.objects.filter(id=user_id).first())


def avatar_test():
    User = get_user_model()
    user = User.objects.get(id=2)
    print(user.customuser.avatars.url)


def delete_guoji():
    Empty_Classroom.objects.filter(campus='3').delete()

@task()
def veryslowadd(a, b):
    sleep(3)
    return a + b

# 将所有用户的密码都设为123
def change_all_to_123():
    users = CustomUser.objects.all()
    for user in users:
        user.admin.set_password('123')
        user.save()


# 将classroom中所有的building_id 提取出来一个列表
def list_building_id():
    classrooms = Empty_Classroom.objects.all()
    building_ids = set()
    for classroom in classrooms:
        building_ids.add(classroom.building_id)
    return list(building_ids)

# 将所有“资源共享”的post的post_type改为“资源分享”
def change_resource_share_post_type():
    posts = Post.objects.filter(post_type='资料共享')
    for post in posts:
        post.post_type = '资源分享'
        post.save()

# 给每个用户随机分配第一个学校，华南理工大学，中山大学，西安理工大学，清华大学，广东工业大学，北京大学，华南师范大学
def random_assign_school():
    # 随机分配学校
    import random
    schools = ['华南理工大学', '中山大学', '西安理工大学', '清华大学', '广东工业大学', '北京大学', '华南师范大学']
    users = CustomUser.objects.all()
    for user in users:
        user.school = random.choice(schools)
        user.save()



if __name__ == '__main__':
    random_assign_school()
