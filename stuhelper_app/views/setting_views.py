from blueapps.account.decorators import login_exempt
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from config.default import MEDIA_ROOT
from session.token import generate, session_is_valid
from stuhelper_app.models import CustomUser, Session, PicTest
from stuhelper_app.userbackend import UserBackEnd


@login_exempt
def loginPage(request):
    return render(request, 'login.html')


@login_exempt
def do_login(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        username = request.POST.get('username')
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = UserBackEnd.authenticate(request, username=username,
                                        password=password)
        if user is not None:
            login(request, user)  # id -> sesstion
            # token 认证
            user_matched = CustomUser.objects.filter(admin_id=user.id).first()
            user_id = user_matched.id
            token = generate(user_id)
            response = redirect('welcome_page')
            response.set_cookie('auth_token', token)
            response.set_cookie('your_avatar_path', user_matched.avatars.url)
            return response
        else:
            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')


@login_required
def logout_user(request):
    # 删除token
    user_id = CustomUser.objects.filter(admin_id=request.user.id).first().id
    Session.objects.filter(user=user_id).delete()
    logout(request)
    return redirect('login')


@login_exempt
def personal_profile(request):
    options = ['华南理工大学', '西安理工大学', '中山大学', '华中科技大学', '西安交通大学', '西安工业大学',
               '华南师范大学', '华南农业大学', '北京大学', '清华大学', '复旦大学', '上海交通大学', '武汉大学',
               '浙江大学', '南京大学', '中国科学技术大学', '哈尔滨工业大学', '同济大学', '四川大学', '天津大学',
               '北京航空航天大学', '东南大学', '南开大学', '重庆大学', '西安交通大学', '大连理工大学', '山东大学',
               '吉林大学', '厦门大学', '湖南大学', '中国人民大学', '中南大学', '北京师范大学', '兰州大学',
               '西北工业大学', '华东师范大学', '北京理工大学', '电子科技大学', '东北大学', '华东理工大学',
               '西北农林科技大学', '中国海洋大学', '南京航空航天大学', '北京科技大学', '北京交通大学', '中国矿业大学',
               '华中师范大学', '北京化工大学', '中国农业大学', '中央民族大学', '北京邮电大学', '北京林业大学',
               '中国石油大学', '南京理工大学', '华中农业大学', '西南交通大学', '北京中医药大学', '北京外国语大学',
               '中国地质大学', '中国石油大学', '中国药科大学', '中国地质大学', '中国政法大学', '中央财经大学',
               '北京体育大学', '北京协和医学院', '北京工业大学', '北京联合大学', '北京工商大学', '北京电子科技学院',
               '北京建筑大学', '北京印刷学院', '北京石油化工学院', '北京信息科技大学', '北京服装学院', '深圳大学',
               '广东工业大学', '广州大学', '华南师范大学', '华南理工大学', '暨南大学', '汕头大学', '广东外语外贸大学',
               '广州中医药大学', '广东药科大学', '广东金融学院', '广东商学院', '广东财经大学', '广东警官学院',
               '广州体育学院', '广州美术学院', '星海音乐学院', '广东技术师范学院', '广东培正学院', '仲恺农业工程学院',
               '广东白云学院', '广州医科大学', '广东第二师范学院', '广东医学院', '广东石油化工学院',
               '广东工程职业技术学院', '广东外语外贸大学', '广东机电职业技术学院', '广东交通职业技术学院',
               '广东轻工职业技术学院', '广东水利电力职业技术学院', '广东工贸职业技术学院', '广东司法警官职业学院',
               '广东省外语艺术职业学院', '广东文艺职业学院', '广东南方职业学院', '广东农工商职业技术学院',
               '广东新安职业技术学院', '广东科学技术职业学院', '广东食品药品职业学院', '广东工业大学', ]

    context = {
        'options': options,
    }
    return render(request, 'personal_profile.html', context)


@login_exempt
def upload_handle(request):
    pic = request.FILES['pic']

    save_path = "%s/avatars/%s" % (MEDIA_ROOT, pic.name)

    with open(save_path, 'wb') as f:
        for content in pic.chunks():
            f.write(content)

    PicTest.objects.create(pic='avatars/%s' % pic.name)

    return HttpResponse('上传成功，图片地址:avatars/%s' % pic.name)


@login_exempt
def change_avatar(request):
    pic = request.FILES['pic']

    # 如果是.png 结尾的文件
    if not pic.name.endswith('.png'):
        messages.error(request, "头像修改失败,请上传png格式的图片")
        return redirect('personal_profile')
    if pic.size > 1024 * 1024 * 2:
        messages.error(request, "头像修改失败,图片大小不能超过2M")
        return redirect('personal_profile')
    save_path = "%s/avatars/%s" % (MEDIA_ROOT, pic.name)
    with open(save_path, 'wb') as f:
        for content in pic.chunks():
            f.write(content)
    user = CustomUser.objects.filter(admin_id=request.user.id).first()
    user.avatars = 'avatars/' + pic.name
    user.save()
    messages.success(request, "头像修改成功")
    return redirect('personal_profile')


@login_exempt
def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('personal_profile/')
    else:
        qq = request.POST.get('qq')
        phone = request.POST.get('phone')
        school = request.POST.get('school')
        motto = request.POST.get('motto')
        try:
            user = CustomUser.objects.filter(admin_id=request.user.id).first()
            user.qq = qq
            user.phone = phone
            user.school = school
            user.motto = motto
            user.save()
            messages.success(request, "资料修改成功")

            return redirect('personal_profile/')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('personal_profile/')


@login_exempt
def sign_up(request):
    options = ['华南理工大学', '西安理工大学', '中山大学', '华中科技大学', '西安交通大学', '西安工业大学',
               '华南师范大学', '华南农业大学', '北京大学', '清华大学', '复旦大学', '上海交通大学', '武汉大学',
               '浙江大学', '南京大学', '中国科学技术大学', '哈尔滨工业大学', '同济大学', '四川大学', '天津大学',
               '北京航空航天大学', '东南大学', '南开大学', '重庆大学', '西安交通大学', '大连理工大学', '山东大学',
               '吉林大学', '厦门大学', '湖南大学', '中国人民大学', '中南大学', '北京师范大学', '兰州大学',
               '西北工业大学', '华东师范大学', '北京理工大学', '电子科技大学', '东北大学', '华东理工大学',
               '西北农林科技大学', '中国海洋大学', '南京航空航天大学', '北京科技大学', '北京交通大学', '中国矿业大学',
               '华中师范大学', '北京化工大学', '中国农业大学', '中央民族大学', '北京邮电大学', '北京林业大学',
               '中国石油大学', '南京理工大学', '华中农业大学', '西南交通大学', '北京中医药大学', '北京外国语大学',
               '中国地质大学', '中国石油大学', '中国药科大学', '中国地质大学', '中国政法大学', '中央财经大学',
               '北京体育大学', '北京协和医学院', '北京工业大学', '北京联合大学', '北京工商大学', '北京电子科技学院',
               '北京建筑大学', '北京印刷学院', '北京石油化工学院', '北京信息科技大学', '北京服装学院', '深圳大学',
               '广东工业大学', '广州大学', '华南师范大学', '华南理工大学', '暨南大学', '汕头大学', '广东外语外贸大学',
               '广州中医药大学', '广东药科大学', '广东金融学院', '广东商学院', '广东财经大学', '广东警官学院',
               '广州体育学院', '广州美术学院', '星海音乐学院', '广东技术师范学院', '广东培正学院', '仲恺农业工程学院',
               '广东白云学院', '广州医科大学', '广东第二师范学院', '广东医学院', '广东石油化工学院',
               '广东工程职业技术学院', '广东外语外贸大学', '广东机电职业技术学院', '广东交通职业技术学院',
               '广东轻工职业技术学院', '广东水利电力职业技术学院', '广东工贸职业技术学院', '广东司法警官职业学院',
               '广东省外语艺术职业学院', '广东文艺职业学院', '广东南方职业学院', '广东农工商职业技术学院',
               '广东新安职业技术学院', '广东科学技术职业学院', '广东食品药品职业学院', '广东工业大学', ]
    context = {
        'options': options,
    }
    return render(request, 'sign_up.html', context)


@login_exempt
def change_password(request):
    return render(request, 'change_password.html')


@login_exempt
def do_change_password(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('change_password')
    else:
        # 验证旧密码
        old_password = request.POST.get('original_password')
        user = request.user
        if not user.check_password(old_password):
            messages.error(request, "旧密码错误")
            return redirect('change_password')

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "两次密码不一致")
            return redirect('change_password')
        try:
            user = request.user
            user.set_password(password1)
            user.save()
            messages.success(request, "密码修改成功，请重新登录")
            return redirect('login')
        except:
            messages.error(request, "Failed to Update Password")
            return redirect('change_password')


@login_exempt
def do_register(request):
    if request.method != "POST":
        return HttpResponse("Register Fail!")
    else:
        if request.session['vertify'] != request.POST.get('vertify'):
            messages.error(request, "验证码错误")
            # 将验证码错误的信息返回给前端
            return redirect('sign_up')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        school = request.POST.get('school')
        email = request.POST.get('email')
        # Check for errorneous inputs
        if password1 != password2:
            messages.error(request, "Password do not match")
            return redirect('sign_up')
        try:
            User = get_user_model()
            user = User.objects.create_user(username=username, password=password1)

            cuser = CustomUser.objects.get(admin=user)
            cuser.phone = phone
            cuser.school = school
            cuser.email = email
            user.save()
            cuser.save()
        except Exception as e:
            print(str(e))
            messages.error(request, "Fail! Change the username or contact the administrator")
            return redirect('login')

    messages.success(request, "Register successfully!")
    return redirect('login')


@login_exempt
def check_request(request):
    user_admin_id = request.session.get('_auth_user_id')
    user = CustomUser.objects.filter(admin_id=user_admin_id).first()
    auth_token = request.COOKIES.get('auth_token')
    if not session_is_valid(user.id, auth_token):
        return None
    else:
        return user
