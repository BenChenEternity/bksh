from blueapps.account.decorators import login_exempt
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from stuhelper_app.models import Message, CustomUser, Private_Message
from stuhelper_app.views.views import get_session_list
from stuhelper_app.views.setting_views import check_request


@login_exempt
def my_messages(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    message_records = Message.objects.filter(owner=user.id).all().order_by('-timestamp')
    msgs = []
    for message_record in message_records:
        if message_record.type == 'system':
            message_obj = {
                'type': message_record.type,
                'timestamp': message_record.timestamp,
                'postTitle': message_record.post.title,
                'read': message_record.read
            }
        elif message_record.type == 'follow':
            message_obj = {
                'type': message_record.type,
                'timestamp': message_record.timestamp,
                'userAdminId': message_record.user.admin_id,
                'userName': message_record.user.admin.username,
                'userSchool': message_record.user.school,
                'userAvatar': message_record.user.avatars.url,
                'read': message_record.read
            }
        elif message_record.type == 'like':
            message_obj = {
                'type': message_record.type,
                'timestamp': message_record.timestamp,
                'postId': message_record.post.id,
                'postTitle': message_record.post.title,
                'postBriefContent': message_record.post.brief_content,
                'userAdminId': message_record.user.admin_id,
                'userName': message_record.user.admin.username,
                'userSchool': message_record.user.school,
                'userAvatar': message_record.user.avatars.url,
                'read': message_record.read
            }
        else:  # comment
            message_obj = {
                'type': message_record.type,
                'timestamp': message_record.timestamp,
                'postId': message_record.post.id,
                'postTitle': message_record.post.title,
                'postBriefContent': message_record.post.brief_content,
                'userAdminId': message_record.user.admin_id,
                'userName': message_record.user.admin.username,
                'userSchool': message_record.user.school,
                'userAvatar': message_record.user.avatars.url,
                'read': message_record.read
            }
        msgs.append(message_obj)
        message_record.read = True
        message_record.save()
    context = {
        'msgs': msgs,
    }
    return render(request, 'my_message.html', context)


@login_exempt
def call_messages(request, called_id):
    user = check_request(request)
    if user is None:
        return redirect('login')
    session_list, added_person_ids = get_session_list(request, user)
    called_user_id = int(called_id)
    if called_user_id in added_person_ids:
        # 放到最前面
        for index, person_obj in enumerate(session_list):
            if person_obj.get('person_id') == called_user_id:
                session_list.pop(index)
                session_list.insert(0, person_obj)
                break
    else:
        # 筛选出来
        person_info = CustomUser.objects.filter(id=called_user_id).first()
        person_obj = {
            'person_id': person_info.id,
            'person_admin_id': person_info.admin_id,
            'person_avatar': person_info.avatars.url,
            'person_name': person_info.admin.username,
            'person_school': person_info.school,
            'red_dot': False
        }
        session_list.insert(0, person_obj)
    return session_list


@login_exempt
def private_messages(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    called_user_id = request.GET.get("user_id")
    if called_user_id is None:
        session_list, _ = get_session_list(request, user)
    else:
        session_list = call_messages(request, called_user_id)
    context = {
        'sessions': session_list,
    }
    return render(request, 'private_messages.html', context)


def private_messages_single_user(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    opposite_id = request.POST.get("user_id")
    messages_you_receive = Private_Message.objects.filter(receiver=user.id, sender=opposite_id)
    messages_you_send = Private_Message.objects.filter(receiver=opposite_id, sender=user.id)
    msgs = []
    # 你收到的消息
    for each_message in messages_you_receive:
        each_message_obj = {
            'timestamp': each_message.timestamp,
            'message': each_message.message,
            'you_receive': True,
        }
        msgs.append(each_message_obj)
        each_message.read = True
        each_message.save()
    # 你发送的消息
    for each_message in messages_you_send:
        each_message_obj = {
            'timestamp': each_message.timestamp,
            'message': each_message.message,
            'read': each_message.read,
            'you_receive': False
        }
        msgs.append(each_message_obj)
    msgs = sorted(msgs, key=lambda x: x['timestamp'])
    return JsonResponse({'status_request': 'success', 'msgs': msgs})


def send_private_message(request):
    user = check_request(request)
    if user is None:
        return redirect('login')
    send_user_id = user.id
    receive_user_id = request.POST.get('user_id')
    message = request.POST.get('message')
    timestamp = timezone.now()
    Private_Message.objects.create(sender_id=send_user_id, receiver_id=receive_user_id, message=message,
                                   timestamp=timestamp)
    return JsonResponse({'status_request': 'success', 'message_info': timestamp})
