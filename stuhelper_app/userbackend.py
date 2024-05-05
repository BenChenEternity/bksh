from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class UserBackEnd(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def check_password2(self, phone, raw_password):
        UserModel = get_user_model()

        real_password = UserModel.objects.get(phone=phone).password
        if real_password == raw_password:
            return True
