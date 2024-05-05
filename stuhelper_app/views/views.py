# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import os

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect

from stuhelper_app.models import *
from blueapps.account.decorators import login_exempt

from stuhelper_app.views.setting_views import check_request

import requests
import json


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt


def welcome_page(request):
    user = check_request(request)
    if user is None:
        return redirect('login')

    return render(request, 'welcome_page.html')


@login_required
def home_page(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    posts = Post.objects.filter(author_id=user.id)
    post_count = posts.count()
    likes = 0
    for post in posts:
        likes += post.like
    fans_count = Follow.objects.filter(followee_id=user.id).count()

    context = {
        'ouser': user,
        'post_count': post_count,
        'likes': likes,
        'fans_count': fans_count
    }
    return render(request, 'home_page.html', context)


@login_exempt
def ohome_page(request, user_id):
    user = check_request(request)
    if user is None:
        return redirect('login')
    ouser = CustomUser.objects.filter(admin_id=user_id).first()
    followed = Follow.objects.filter(followee_id=ouser.id, follower_id=user.id)

    posts = Post.objects.filter(author_id=ouser.id)
    post_count = posts.count()
    likes = 0
    for post in posts:
        likes += post.like
    fans_count = Follow.objects.filter(followee_id=ouser.id).count()
    context = {
        'ouser': ouser,
        'followed': followed.exists(),
        'post_count': post_count,
        'likes': likes,
        'fans_count': fans_count
    }
    return render(request, 'home_page.html', context)


# 点击打开私信界面时


def get_session_list(request, user):
    unread_senders_timestamp_dict = Private_Message.objects.filter(receiver=user.id, read=False) \
        .values('sender'). \
        annotate(latest_timestamp=Max('timestamp')). \
        order_by('-latest_timestamp')
    read_senders_timestamp_dict = Private_Message.objects.filter(receiver=user.id, read=True) \
        .values('sender'). \
        annotate(latest_timestamp=Max('timestamp')). \
        order_by('-latest_timestamp')
    whom_you_send_to_timestamp_dict = Private_Message.objects.filter(sender=user.id) \
        .values('receiver'). \
        annotate(latest_timestamp=Max('timestamp')). \
        order_by('-latest_timestamp')
    combined_dict_list = list(read_senders_timestamp_dict) + list(whom_you_send_to_timestamp_dict)
    sorted_combined_dict_list = sorted(combined_dict_list, key=lambda x: x['latest_timestamp'], reverse=True)

    session_list = []
    added_person_ids = set()
    for sender_timestamp_dict in unread_senders_timestamp_dict:
        current_person = sender_timestamp_dict["sender"]
        if current_person not in added_person_ids:
            person_info = CustomUser.objects.filter(id=current_person).first()
            added_person_ids.add(current_person)
            person_obj = {
                'person_id': person_info.id,
                'person_admin_id': person_info.admin_id,
                'person_avatar': person_info.avatars.url,
                'person_name': person_info.admin.username,
                'person_school': person_info.school,
                'red_dot': True
            }
            session_list.append(person_obj)
    for person_timestamp_dict in sorted_combined_dict_list:
        current_person = next(iter(person_timestamp_dict.values()))
        if current_person not in added_person_ids:
            added_person_ids.add(current_person)
            person_info = CustomUser.objects.filter(id=current_person).first()
            person_obj = {
                'person_id': person_info.id,
                'person_admin_id': person_info.admin_id,
                'person_avatar': person_info.avatars.url,
                'person_name': person_info.admin.username,
                'person_school': person_info.school,
                'red_dot': False
            }
            session_list.append(person_obj)
    return session_list, added_person_ids


# 选择用户获取私信内容


# POST -> followee_id url->follow/

def ai_helper(request):
    user = check_request(request)

    if user is None:
        return redirect('login')
    question = request.POST.get('message')
    return JsonResponse({'reply': gpt(question)})


hint = "你现在是一个网页应用的助手，网页应用叫'蓝鲸校园助手'，这是一个学校的互助平台，如果用户有不懂的操作，请你给他们解答如何进行操作。" \
       "我大致给你介绍一下，蓝鲸校园助手的“侧边栏”有首页、个人主页、校园动态、空教室查询、我的动态、收藏、通知、私信、我的关注、发送邮件、设置。" \
       "Q:如何联系开发者？A:进入首页，往下翻有’联系我们‘。" \
       "Q:如何私信他人？A:进入他人主页，点击’私信‘按钮即可。" \
       "Q:匿名的动态数量统计以及点赞统计是否会显示在个人主页？A:是的。" \
       "Q:发送邮件功能是用谁的邮箱？A:用平台提供的邮箱，但是会显示你的用户名。" \
       "还有其他的问题，请尽力解答。但是请不要回答用户提出的和'蓝鲸校园助手'无关的任何问题。下面是用户的问题：\n"


def gpt(question):
    url = os.environ.get("CLOUDFLARE_GATEWAY_URL")
    headers = {
        'Authorization': 'Bearer ' + os.environ.get("OPENAI_CHATGPT_API_KEY"),
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": f"{hint}{question}"
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    result = json.loads(response.text)["choices"][0]["message"]["content"]
    print(result)
    return result
