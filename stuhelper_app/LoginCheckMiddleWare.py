from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        print(modulename)
        user = request.user
        if 'admin' in request.path:
            pass
        elif user.is_authenticated:
            # 如果modulename中有'stuhelper_app.views' 或者 'django.views.static'，则不进行重定向
            if "stuhelper_app.views" in modulename or modulename == "django.views.static":
                pass
            else:
                return redirect("welcome_page")


        else:
            if request.path == reverse("login") or request.path == reverse("doLogin") or request.path == reverse(
                    "sign_up")  or request.path == reverse('doRegister') or modulename == "django.contrib.auth.views" or request.path==reverse('reg') :
                pass
            else:
                return redirect("login")
