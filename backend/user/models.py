import os
import random

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


def get_avatar_path(instance, filename):
    upload_to = os.path.join('avatar', instance.username)

    return os.path.join(upload_to, filename)


class User(AbstractUser):
    avatar = ProcessedImageField(upload_to=get_avatar_path, default='avatar/default.png', verbose_name='头像',
                                 processors=[ResizeToFill(64, 64)], blank=True
                                 )

    def __str__(self):
        return self.username


class VerificationCode(models.Model):
    email = models.EmailField(max_length=100, unique=True, db_index=True, null=False)
    code = models.IntegerField(null=False)

    @staticmethod
    def generate_code(email):
        item = VerificationCode.objects.filter(email=email).first()
        if item is None:
            item = VerificationCode(email=email)
        code = random.randint(1000, 9999)
        item.code = code
        item.save()

        send_mail(
            subject="Memorest 验证码",
            from_email="memorest@email.streack.cn",
            message="您的验证码为：" + str(code),
            recipient_list=(
                    email,
            ),
            fail_silently=False,
        )

        return item

