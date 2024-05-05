from datetime import datetime

from blueapps.account.decorators import login_exempt
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Func, Count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView

from stuhelper_app.models import Empty_Classroom
from stuhelper_app.models import *


class LeftSubstring(Func):
    function = 'LEFT'
    template = '%(function)s(%(expressions)s, 10)'
    output_field = models.CharField()


def admin_home(request):
    posts_count_list_in_category = []
    category_name_list = ['打听求助', "扩列交友", "二手买卖", "心灵树洞", '资源分享']

    user_count = CustomUser.objects.all().count()
    moment_count = Post.objects.all().count()
    empty_classroom_count = Empty_Classroom.objects.all().count()
    message_count = Private_Message.objects.all().count()

    for category in category_name_list:
        posts_count = Post.objects.filter(post_type=category).count()
        posts_count_list_in_category.append(posts_count)

    post_data = (
        Post.objects.annotate(date=LeftSubstring('ctime'))
        .values('date')
        .annotate(count=Count('id'))
    )
    for post in post_data:
        # 将字符串日期转换为 datetime 对象
        post['date'] = datetime.strptime(post['date'], '%Y-%m-%d')
    # Extract dates and counts from the query result
    post_data = sorted(post_data, key=lambda x: x['date'])
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in post_data]
    counts = [entry['count'] for entry in post_data]

    context = {
        'posts_count_list_in_category': posts_count_list_in_category,
        'category_name_list': category_name_list,
        'user_count': user_count,
        'moment_count': moment_count,
        'empty_classroom_count': empty_classroom_count,
        'message_count': message_count,
        'dates': dates,
        'counts': counts,
    }
    return render(request, 'admin_templates/home_content.html', context)


class PostListView(ListView):
    queryset = Post.objects.all()
    template_name = 'admin_templates/post_list.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def moment_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    messages.success(request, "Delete successfully!")
    return redirect('manage_post')