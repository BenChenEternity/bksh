from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

import settings
from blueapps.account.components.bk_token.models import UserProxy


class CustomUser(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=20, null=True, unique=True)
    qq = models.CharField(max_length=20, null=True)
    avatars = models.ImageField(upload_to='avatars', default='avatars/lazy_cat.jpg')
    school = models.CharField(max_length=20, null=True)
    motto = models.CharField(max_length=50, null=True, default='这个人很懒，什么都没有留下')
    anonymous_img = models.CharField(max_length=50, default='avatars/anonymous.jpg')
    REQUIRED_FIELDS = ['phone', 'username']
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = False

    def __str__(self):
        return self.admin.username


class Empty_Classroom(models.Model):
    classroom_type_data = (('1', "普通教室"), ('2', "智慧教室"))
    campus_data = (('1', '大学城校区'), ('2', '五山校区'), ('3', '国际校区'))
    location_id = models.CharField(max_length=20, null=True)
    building_id = models.CharField(max_length=20, null=True)
    floor_id = models.IntegerField(default=1)
    seat_num = models.IntegerField(default=1)
    exam_seat_num = models.IntegerField(null=True)
    classroom_type = models.CharField(default=1, choices=classroom_type_data, max_length=10)
    empty_week = models.CharField(max_length=20, null=True, default="1")
    empty_day = models.CharField(max_length=20, null=True, default="1")
    empty_session = models.IntegerField(null=True, default=1)
    campus = models.CharField(default='1', choices=campus_data, max_length=10)

    def __str__(self):
        return self.location_id


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    hash_id = models.CharField(max_length=16, null=True)  # 唯一哈希码
    title = models.CharField(max_length=20, null=True)
    content = models.TextField(null=True)
    post_type = models.CharField(max_length=16, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=6)
    ctime = models.DateTimeField(auto_now_add=True, null=True)
    like = models.IntegerField(default=0)
    anonymous = models.BooleanField(default=False)
    star = models.IntegerField(default=0)
    brief_content = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.title


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField(default=0)
    session_token = models.CharField(max_length=32, null=True)
    expire_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        # 如果 expire_date 为空，则设置为当前时间 + 30 分钟
        if not self.expire_date:
            self.expire_date = timezone.now() + timezone.timedelta(hours=8, minutes=30)
        super().save(*args, **kwargs)


class User_Like_Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} likes {self.post.title}'


class User_Star_Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} likes {self.post.title}'


class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')
    followee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followee')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} follows {self.followee}'


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.IntegerField(null=True)
    type = models.CharField(max_length=16, null=True)  # like follow system(comment)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 谁引发的消息
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)  # 消息相关的帖子
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type}: {self.user} -> {self.post.title}'


class Private_Message(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="who_send_this")  # 发送者
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="who_receive_this")  # 接收者
    message = models.CharField(max_length=256, null=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} ---private message---> {self.receiver}  : {self.message}'


class Comment_Post(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f'{self.commenter} ---comment post---> {self.post}  : {self.message}'


class PicTest(models.Model):
    pic = models.ImageField(upload_to='booktest/')

    def __str__(self):
        return self.pic.name


@receiver(post_save, sender=UserProxy)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(admin=instance)


@receiver(post_save, sender=UserProxy)
def save_user_profile(sender, instance, **kwargs):
    instance.customuser.save()
