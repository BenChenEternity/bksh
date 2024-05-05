import random

import django
import requests
from blueapps.account.decorators import login_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import settings
from stuhelper_app.models import CustomUser


@login_exempt
def email_module(request):
    return render(request, 'user_email_send.html')


@login_exempt
def send_sms_code(request, to_email):
    """
    发送邮箱验证码
    :param to_mail: 发到这个邮箱
    :return: 成功：0 失败 -1
    """
    response = {"status": False, "msg": ""}

    try:
        sms_code = '%06d' % random.randint(0, 999999)
        title = '邮箱激活'
        content = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)
        to_email = to_email

        response = requests.post(
            url=f"{django.conf.settings.BK_COMPONENT_API_URL}/api/c/compapi/cmsi/send_mail/",
            json={
                "bk_app_code": settings.APP_CODE,
                "bk_app_secret": settings.SECRET_KEY,
                "bk_token": request.COOKIES.get("bk_token"),
                "receiver": to_email,
                "title": title,
                "content": content,
            }
        )

        send_result = response.json()
        if send_result['result']:
            return sms_code
        else:
            return

    except:
        send_status = -1
        response['status'] = 'fail'
    print(response)
    return JsonResponse(response)


@login_exempt
def existUser(email):
    created = 1
    try:
        CustomUser.objects.get(email=email)
    except:
        created = 0
    return created


def reg(request):
    if request.POST.get('type') == 'sendMessage':
        print(request.POST.get('email'))
        email = request.POST.get('email')
        response = {"state": False, "errmsg": ""}

        if existUser(email):
            response['errmsg'] = '该用户已存在，请登录'
        else:
            try:
                sms_code = send_sms_code(request, email)  # 发送邮件
                request.session['vertify'] = sms_code  # 验证码存入session，用于做注册验证
                response['state'] = True
                response['susmsg'] = '验证码发送成功，请注意查收'
            except:
                response['errmsg'] = '验证码发送失败，请检查邮箱地址' + email
        return JsonResponse(response)
    return HttpResponse('Error')


@login_exempt
def email_change(request):
    return render(request, 'email_module.html')


@login_exempt
def confirm_email(request):
    if request.POST.get('type') == 'confirmMessage':

        vertify = request.POST.get('vertify')
        response = {"state": False, "errmsg": ""}

        if vertify == request.session['vertify']:
            user = CustomUser.objects.filter(admin_id=request.user.id).first()
            user.email = request.POST.get('email')
            user.save()
            response['status'] = 'success'
        else:
            print('no')
            response['status'] = 'error'
        return JsonResponse(response)
    return HttpResponse('?>?')


@login_exempt
def send_email(request):
    response = {"status": False, "msg": ""}

    try:
        user = CustomUser.objects.filter(admin_id=request.user.id).first()
        username = user.admin.username
        to_email = request.POST.get('to_email')
        brief = f'<html><h3>本邮件由蓝鲸校园助手"{username}"发给您：</h3> </html>'
        title = request.POST.get('title')
        content = request.POST.get('content')
        content = brief + '<p>' + content + '</p>'
        response = requests.post(
            url=f"{django.conf.settings.BK_COMPONENT_API_URL}/api/c/compapi/cmsi/send_mail/",
            json={
                "bk_app_code": settings.APP_CODE,
                "bk_app_secret": settings.SECRET_KEY,
                "bk_token": request.COOKIES.get("bk_token"),
                "receiver": to_email,
                "title": title,
                "content": content,
            }
        )
        send_result = response.json()
        if send_result['result']:
            return JsonResponse({"result": True, 'status': 'success'})
        else:
            return JsonResponse({"result": False, 'status': 'fail'})
        # email_body = content
        # user = CustomUser.objects.filter(admin_id=request.user.id).first()
        # email_from = settings.EMAIL_HOST_USER
        # username = user.admin.username
        # email_title = '来自' + username + '的邮件：' + title
        #
        # send_status = send_mail(email_title, email_body, email_from, [to_email])
        # response['status'] = 'success'
        # print('send_email send ok')
    except:
        send_status = -1
        response['status'] = 'fail'
    print(response)
    return JsonResponse(response)
