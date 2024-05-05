from blueapps.account.decorators import login_exempt
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.utils import IntegrityError

from stuhelper_app.models import Post, User_Like_Post, User_Star_Post, Message, CustomUser, Follow, Comment_Post
from stuhelper_app.views.setting_views import check_request


# 查看动态详情
def view_moment(request, moment_id):
    user = check_request(request)
    post = Post.objects.get(id=moment_id)
    liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
    liked = liked_record.exists()
    starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id)
    starred = starred_record.exists()
    comments = Comment_Post.objects.filter(post_id=post.id).order_by('-timestamp')
    comment_list = []
    for comment in comments:
        comment_list.append(
            {'user_name': comment.commenter.admin.username,
             'user_avatar': comment.commenter.avatars.url,
             'user_admin_id': comment.commenter.admin_id,
             'commenter_school': comment.commenter.school,
             'timestamp': comment.timestamp,
             'message': comment.message})
    context = {
        'post': post,
        'liked': liked,
        'starred': starred,
        'comments': comment_list
    }
    return render(request, 'view_moment.html', context)


# 查看动态分类-打听求助
def moment_help(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    posts = Post.objects.filter(post_type="打听求助").order_by('-ctime')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts_in_page = paginator.page(page)
    except PageNotAnInteger:
        posts_in_page = paginator.page(1)
    except EmptyPage:
        posts_in_page = None
    posts_info = []
    for post in posts_in_page:
        liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
        liked = liked_record.exists()
        starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id)
        starred = starred_record.exists()
        post_info = {
            'post': post,
            'liked': liked,
            'starred': starred
        }
        posts_info.append(post_info)
    context = {
        'posts_info': posts_info,
    }
    return render(request, 'moments.html', context)


def moment_treehole(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    posts = Post.objects.filter(post_type="心灵树洞").order_by('-ctime')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts_in_page = paginator.page(page)
    except PageNotAnInteger:
        posts_in_page = paginator.page(1)
    except EmptyPage:
        posts_in_page = None
    posts_info = []
    for post in posts_in_page:
        liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
        liked = liked_record.exists()
        starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id)
        starred = starred_record.exists()
        post_info = {
            'post': post,
            'liked': liked,
            'starred': starred
        }
        posts_info.append(post_info)
    context = {
        'posts_info': posts_info,
    }
    return render(request, 'moments.html', context)


# 查看动态分类-文件共享
@login_exempt
def moment_share(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    posts = Post.objects.filter(post_type="资源分享").order_by('-ctime')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts_in_page = paginator.page(page)
    except PageNotAnInteger:
        posts_in_page = paginator.page(1)
    except EmptyPage:
        posts_in_page = None
    posts_info = []
    for post in posts_in_page:
        liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
        liked = liked_record.exists()
        starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id)
        starred = starred_record.exists()
        post_info = {
            'post': post,
            'liked': liked,
            'starred': starred
        }
        posts_info.append(post_info)
    context = {
        'posts_info': posts_info
    }
    return render(request, 'moments.html', context)


# 查看动态分类-二手闲置
@login_exempt
def moment_market(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    posts = Post.objects.filter(post_type="二手闲置").order_by('-ctime')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts_in_page = paginator.page(page)
    except PageNotAnInteger:
        posts_in_page = paginator.page(1)
    except EmptyPage:
        posts_in_page = None
    posts_info = []
    for post in posts_in_page:
        liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
        liked = liked_record.exists()
        starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id)
        starred = starred_record.exists()
        post_info = {
            'post': post,
            'liked': liked,
            'starred': starred
        }
        posts_info.append(post_info)
    context = {
        'posts_info': posts_info,

    }
    return render(request, 'moments.html', context)


# 查看动态分类-扩列交友
@login_exempt
def moment_friend(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    posts = Post.objects.filter(post_type="扩列交友").order_by('-ctime')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts_in_page = paginator.page(page)
    except PageNotAnInteger:
        posts_in_page = paginator.page(1)
    except EmptyPage:
        posts_in_page = None
    posts_info = []
    for post in posts_in_page:
        liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
        liked = liked_record.exists()
        starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id)
        starred = starred_record.exists()
        post_info = {
            'post': post,
            'liked': liked,
            'starred': starred
        }
        posts_info.append(post_info)
    context = {
        'posts_info': posts_info,

    }
    return render(request, 'moments.html', context)


# 动态列表
@login_exempt
def moments(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    posts = Post.objects.all().order_by('-ctime')
    paginator = Paginator(posts, 10)  # 每页显示10篇动态
    page = request.GET.get('page')
    try:
        posts_in_page = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，则传递第一页。
        posts_in_page = paginator.page(1)
    except EmptyPage:
        posts_in_page = None
    posts_info = []
    for post in posts_in_page:
        liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
        liked = liked_record.exists()
        starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id)
        starred = starred_record.exists()
        post_info = {
            'post': post,
            'liked': liked,
            'starred': starred
        }
        posts_info.append(post_info)
    context = {
        'posts_info': posts_info,

    }
    return render(request, 'moments.html', context)


# 点赞动态
@login_exempt
def moment_like(request):
    if request.method == 'POST':
        user = check_request(request)
        if user is None:
            return redirect('login')
        post_id = request.POST.get('post_id')
        # 点赞逻辑
        try:
            try:
                like_record = User_Like_Post.objects.get(user=user.id, post=post_id)
                # 点过赞了，执行取消点赞逻辑
                post = like_record.post
                post.like -= 1
                post.save()
                like_record.delete()
                if not user.id == post.author.id:  # 判断是不是给自己取消点赞
                    # 删除点赞通知
                    Message.objects.filter(type='like', post_id=post.id, user_id=user.id).delete()
                return JsonResponse({'result': 'unliked'})
            except User_Like_Post.DoesNotExist:
                # 没有点赞过，执行点赞逻辑
                post = Post.objects.get(id=post_id)
                post.like += 1
                post.save()
                User_Like_Post.objects.create(user_id=user.id, post_id=post.id, timestamp=timezone.now())
                if not user.id == post.author.id:  # 判断是不是给自己点赞，如果是就不发通知
                    # 发送点赞通知给题主
                    Message.objects.create(type='like', post_id=post.id, user_id=user.id, owner=post.author.id,
                                           timestamp=timezone.now())
                return JsonResponse({'result': 'liked'})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# 收藏动态
@login_exempt
def moment_star(request):
    if request.method == 'POST':
        user = check_request(request)
        if user is None:
            return redirect('login')
        post_id = request.POST.get('post_id')

        try:
            try:
                # 按照id查找收藏记录
                star_record = User_Star_Post.objects.get(user=user.id, post=post_id)

                # 取消收藏
                star_record.delete()
                return JsonResponse({'result': 'unstarred'})
            except User_Star_Post.DoesNotExist:
                # 收藏
                post = Post.objects.get(id=post_id)
                User_Star_Post.objects.create(user_id=user.id, post_id=post.id, timestamp=timezone.now())
                return JsonResponse({'result': 'starred'})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# 发布动态
def moment_publish(request):
    category = {
        "打听求助",
        "扩列交友",
        "二手买卖",
        "心灵树洞",
    }
    context = {
        'category': category,
    }

    return render(request, 'moment_publish.html', context)


# 我的动态
def my_moment(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    posts = Post.objects.filter(author_id=user.id).order_by('-ctime')
    posts_info = []
    for post in posts:
        liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
        liked = liked_record.exists()
        starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id)
        starred = starred_record.exists()
        post_info = {
            'post': post,
            'liked': liked,
            'starred': starred
        }
        posts_info.append(post_info)
    context = {
        'posts_info': posts_info,

    }
    return render(request, 'my_moment.html', context)


# 他人动态
def others_moment(request, user_id):
    user = check_request(request)
    if user is None:
        return redirect('login')
    author_id = CustomUser.objects.filter(admin_id=user_id).first().id
    posts = Post.objects.filter(author_id=author_id, anonymous=False).all().order_by('-ctime')
    paginator = Paginator(posts, 10)  # 每页显示10篇动态
    page = request.GET.get('page')
    try:
        posts_in_page = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，则传递第一页。
        posts_in_page = paginator.page(1)
    except EmptyPage:
        posts_in_page = None
    posts_info = []
    for post in posts_in_page:
        liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
        liked = liked_record.exists()
        starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id)
        starred = starred_record.exists()
        post_info = {
            'post': post,
            'liked': liked,
            'starred': starred,

        }
        posts_info.append(post_info)
    context = {
        'posts_info': posts_info,

    }
    return render(request, 'others_moments.html', context)


# 删除我的一条动态
def my_moment_delete(request, post_id):
    user = check_request(request)
    if user is None:
        return redirect('login')
    post = Post.objects.filter(id=post_id)
    try:
        post.delete()
        messages.success(request, "动态删除成功")
    except Post.DoesNotExist:
        messages.error(request, "删除失败:动态不存在")
    except:
        messages.error(request, "删除失败")
    else:
        return redirect('my_moment')


# 我的收藏
def my_star(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    posts = Post.objects.filter(
        id__in=User_Star_Post.objects.filter(user_id=user.id).values_list('post_id', flat=True)).order_by(
        'user_star_post__timestamp')
    paginator = Paginator(posts, 10)  # 每页显示10篇动态
    page = request.GET.get('page')
    try:
        posts_in_page = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，则传递第一页。
        posts_in_page = paginator.page(1)
    except EmptyPage:
        posts_in_page = None
    posts_info = []
    for post in posts_in_page:
        liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
        liked = liked_record.exists()

        # 按照id查找收藏记录

        starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id).order_by('id')
        starred = starred_record.exists()
        post_info = {
            'post': post,
            'liked': liked,
            'starred': starred
        }
        posts_info.append(post_info)
    context = {
        'posts_info': posts_info,

    }
    return render(request, 'my_star.html', context)


# 关注他人
def follow(request):
    if request.method == 'POST':
        user = check_request(request)
        if user is None:
            return redirect('login')
        followee_id = CustomUser.objects.filter(admin_id=request.POST.get("followee_id")).first().id
        # 关注逻辑
        if user.id == followee_id:
            # 自己关注自己，拒绝
            return JsonResponse({'result': 'reject'})
        try:
            try:
                follow_record = Follow.objects.get(follower_id=user.id, followee_id=followee_id)
                # 关注过了，执行取消关注逻辑
                follow_record.delete()
                # 发送关注通知给题主
                Message.objects.filter(type='follow', user_id=user.id, owner=followee_id).delete()
                return JsonResponse({'result': 'unfollowed'})
            except Follow.DoesNotExist:
                # 没有关注过，执行关注逻辑
                Follow.objects.create(follower_id=user.id, followee_id=followee_id, timestamp=timezone.now())
                # 发送关注通知给题主
                Message.objects.create(type='follow', user_id=user.id, owner=followee_id,
                                       timestamp=timezone.now())
                return JsonResponse({'result': 'followed'})
        except Follow.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# 我的关注
def my_follows(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    follow_records = Follow.objects.filter(follower_id=user.id).all().order_by('-timestamp')
    followings = []
    for follow_record in follow_records:
        followee = CustomUser.objects.filter(id=follow_record.followee_id).first()
        followee_obj = {
            'followee_id': followee.id,
            'followee_admin_id': followee.admin_id,
            'followee_avatar': followee.avatars.url,
            'followee_name': followee.admin.username,
            'followee_school': followee.school
        }
        followings.append(followee_obj)
    context = {
        'followings': followings,
    }
    return render(request, 'my_followings.html', context)


# 关注列表，切换被关注人
def moment_following(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    author_id = request.POST.get('user_id')
    posts = Post.objects.filter(author_id=author_id, anonymous=False).all().order_by('-ctime')
    posts_info = []
    for post in posts:
        liked_record = User_Like_Post.objects.filter(user=user.id, post=post.id)
        liked = liked_record.exists()
        starred_record = User_Star_Post.objects.filter(user=user.id, post=post.id)
        starred = starred_record.exists()
        formatted_time = post.ctime.strftime('%Y-%m-%d %H:%M')
        chinese_formatted_time = formatted_time.replace('-', '年', 1).replace('-', '月', 1).replace(' ', '日 ')
        post_info = {
            'id': post.id,
            'title': post.title,
            'time': chinese_formatted_time,
            'type': post.post_type,
            'content': post.content,
            'like_count': post.like,
            'liked': liked,
            'starred': starred
        }
        posts_info.append(post_info)
    return JsonResponse({'status_request': 'success', 'posts_info': posts_info})


def moment_publish_save(request):
    if request.method != "POST":
        return HttpResponse("Register Fail!")
    else:
        title = request.POST.get('moment_title')
        content = request.POST.get('moment_content')
        brief_content = content[:20] + '...'
        category = request.POST.get('category')
        anonymous = request.POST.get('anonymous', '0')
        user = CustomUser.objects.filter(admin_id=request.user.id).first()
        # 如果content的长度超过了2000，就截取前2000个字符
        if len(content) > 1000:
            content = content[:1000]

        try:
            post = Post.objects.create(title=title, content=content, post_type=category, anonymous=int(anonymous),
                                       author=user, brief_content=brief_content)

            post.save()
        except Exception as e:
            print(str(e))
            messages.error(request, "Fail! Change the username or contact the administrator")
            return redirect('moment_publish')
    messages.success(request, "发布成功！")
    return redirect('moments')


# 资源共享
def do_resource_share(request):
    if request.method != "POST":
        return HttpResponse("Resouce share Fail!")
    else:
        title = request.POST.get('resource_title')
        info = request.POST.get('resource_info')

        category = '资源分享'
        brief_content = info[:20] + '...'
        user = CustomUser.objects.filter(admin_id=request.user.id).first()
        # 如果content的长度超过了2000，就截取前2000个字符
        if len(info) > 300:
            info = info[:300]

        try:
            post = Post.objects.create(title=title, content=info, post_type=category, anonymous=int(0),
                                       author=user, brief_content=brief_content)

            post.save()
        except Exception as e:
            print(str(e))
            messages.error(request, "Fail! Change the username or contact the administrator")
            return redirect('resource_share')
    messages.success(request, "发布成功！")
    return redirect('moments')


def resource_share(request):
    return render(request, 'resource_share.html')


# 发送评论
def send_comment(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    comment_post_id = request.POST.get('post_id')
    message = request.POST.get('message')
    try:
        post_being_comment = Post.objects.filter(id=comment_post_id).first()
        timestamp = timezone.now()
        # 增加评论记录
        Comment_Post.objects.create(commenter_id=user.id, post_id=comment_post_id, message=message, timestamp=timestamp)
        # 通知被评论者
        Message.objects.create(type='comment', post_id=comment_post_id, user_id=user.id,
                               owner=post_being_comment.author.id,
                               timestamp=timestamp)
        return JsonResponse({'result': 'commented'})
    except Post.DoesNotExist:
        # POST没找到
        return JsonResponse({'error': 'Post not found'}, status=404)
    except IntegrityError:
        #  插入失败
        return JsonResponse({'error': 'Comment operation is forbidden'}, status=403)
