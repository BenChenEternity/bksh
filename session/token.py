import random
import threading
import time

from django.utils import timezone

from stuhelper_app.models import Session


def clear_all():
    Session.objects.all().delete()


def generate(user_id):
    if Session.objects.filter(user=user_id).exists():
        logout(user_id)
    characters = 'abcdefghijklmnopqrstuvwxyz1234567890'
    token = ''.join(random.choice(characters) for _ in range(32))
    Session.objects.create(user=user_id, session_token=token)
    return token


def logout(user_id):
    Session.objects.filter(user=user_id).delete()


def session_is_valid(user_id, session_token):
    session = Session.objects.filter(user=user_id, session_token=session_token)
    return session.exists()


def create_token_auto_clear_thread():
    interval_minutes = 1440
    timer_thread = threading.Thread(target=timer, args=(interval_minutes,))
    timer_thread.daemon = True  # 将线程设置为守护线程，当主线程退出时，该线程也会退出
    timer_thread.start()


def timer(interval_minutes):
    while True:
        clear_token()
        time.sleep(interval_minutes * 60)  # 休眠指定的分钟数


def clear_token():
    current_time = timezone.now() + timezone.timedelta(hours=8)
    expired_sessions = Session.objects.filter(expire_date__lt=current_time)
    print(f"token清理{expired_sessions.count()}个")
    expired_sessions.all().delete()

