from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
import stuhelper_app.views.classroom_views
import stuhelper_app.views.email_views
import stuhelper_app.views.messages_views
import stuhelper_app.views.moment_views
import stuhelper_app.views.setting_views
import stuhelper_app.views.gpt_views
import stuhelper_app.views.admin_views
from stuhelper_app.views import views
from .views import admin_views
urlpatterns = (
    # 登录注册
    path('logout_user/', stuhelper_app.views.setting_views.logout_user, name='logout_user'),
    path('', stuhelper_app.views.setting_views.loginPage, name='login'),
    path('change_password/', stuhelper_app.views.setting_views.change_password, name='change_password'),
    path('do_change_password/', stuhelper_app.views.setting_views.do_change_password, name='do_change_password'),
    path('login/', stuhelper_app.views.setting_views.do_login, name='doLogin'),
    path('sign_up/', stuhelper_app.views.setting_views.sign_up, name='sign_up'),
    path('doRegister/', stuhelper_app.views.setting_views.do_register, name='doRegister'),

    # AI小助手
    path('ai_helper/', views.ai_helper, name='ai_helper'),

    # 欢迎页
    path('welcome_page/', views.welcome_page, name='welcome_page'),

    # 主页
    path('home_page/', views.home_page, name='home_page'),
    path('ohome_page/<user_id>', views.ohome_page, name='ohome_page'),

    # 空教室
    path('empty_classroom_search/', stuhelper_app.views.classroom_views.empty_classroom_search,
         name='empty_classroom_search'),
    path('empty_classroom/', stuhelper_app.views.classroom_views.empty_classroom, name='empty_classroom'),

    # 校园动态
    path('moments/', stuhelper_app.views.moment_views.moments, name='moments'),
    path('moment_publish/', stuhelper_app.views.moment_views.moment_publish, name='moment_publish'),
    path('moment_publish_save/', stuhelper_app.views.moment_views.moment_publish_save, name='moment_publish_save'),
    path('view_moment/<moment_id>', stuhelper_app.views.moment_views.view_moment, name='view_moment'),

    # 评论
    path('comment/', stuhelper_app.views.moment_views.send_comment, name='send_comment'),

    # 资源
    path('resource_share/', stuhelper_app.views.moment_views.resource_share, name='resource_share'),
    path('do_resource_share/', stuhelper_app.views.moment_views.do_resource_share, name='do_resource_share'),

    # 分类
    path('moment/help/', stuhelper_app.views.moment_views.moment_help, name='moment_help'),
    path('moment/file_share/', stuhelper_app.views.moment_views.moment_share, name='moment_file_share'),
    path('moment/market/', stuhelper_app.views.moment_views.moment_market, name='moment_market'),
    path('moment/make_friend/', stuhelper_app.views.moment_views.moment_friend, name='moment_make_friend'),
    path('moment_treehole/', stuhelper_app.views.moment_views.moment_treehole, name='moment_treehole'),

    # 动态点赞
    path('moment_like/', stuhelper_app.views.moment_views.moment_like, name='moment_like'),
    path('moment_star/', stuhelper_app.views.moment_views.moment_star, name='moment_star'),

    # 我的动态
    path('my_moment/', stuhelper_app.views.moment_views.my_moment, name='my_moment'),
    path('my_moment_delete/<post_id>', stuhelper_app.views.moment_views.my_moment_delete, name='my_moment_delete'),
    # 他人的动态
    path('others_moment/<user_id>/', stuhelper_app.views.moment_views.others_moment, name='others_moment'),

    # 我的收藏
    path('my_star/', stuhelper_app.views.moment_views.my_star, name='my_star'),

    # 我的关注
    path('follow/', stuhelper_app.views.moment_views.follow, name='follow'),
    path('my_follows/', stuhelper_app.views.moment_views.my_follows, name='my_follows'),
    path('moment_following/', stuhelper_app.views.moment_views.moment_following, name='moment_following'),

    # 通知
    path('my_messages/', stuhelper_app.views.messages_views.my_messages, name='my_messages'),

    # 私信
    path('private_messages/', stuhelper_app.views.messages_views.private_messages, name='private_messages'),
    path('private_messages_single_user/', stuhelper_app.views.messages_views.private_messages_single_user,
         name='private_messages_single_user'),
    path('send_private_message/', stuhelper_app.views.messages_views.send_private_message, name='send_private_message'),

    # 邮件
    path('email/', stuhelper_app.views.email_views.email_module, name='email_module'),
    path('send_sms_code/', stuhelper_app.views.email_views.send_sms_code, name='send_sms_code'),
    path('reg/', stuhelper_app.views.email_views.reg, name='reg'),
    path('confirm/', stuhelper_app.views.email_views.confirm_email, name='confirm_email'),
    path('send_email/', stuhelper_app.views.email_views.send_email, name='send_email'),

    # 个人中心
    path('personal_profile/', stuhelper_app.views.setting_views.personal_profile, name='personal_profile'),
    path('upload_handle/', stuhelper_app.views.setting_views.upload_handle, name='upload_handle'),
    path('change_avatar/', stuhelper_app.views.setting_views.change_avatar, name='change_avatar'),
    path('admin_profile_update', stuhelper_app.views.setting_views.admin_profile_update, name='admin_profile_update'),
    path('email_change/', stuhelper_app.views.email_views.email_change, name='email_change'),
    # 测试

    # gpt
    path('gpt/', stuhelper_app.views.gpt_views.gpt_page, name='gpt_page'),

    url(r'^favicon\.ico$', RedirectView.as_view(url=r'static/img/favicon.ico')),

    # admin_views
    path('admin_homeiii/', admin_views.admin_home, name='admin_home'),
    path('manage_postiii/', admin_views.PostListView.as_view(), name='manage_post'),
    path('moment_deleteiii/<post_id>', admin_views.moment_delete, name='moment_delete'),

)
