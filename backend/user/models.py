import datetime
import os
import random
from smtplib import SMTPException

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
    last_updated = models.DateTimeField(auto_now=True)
    is_last_mail_successful = models.BooleanField(default=False)

    @staticmethod
    def generate_code(email):
        item = VerificationCode.objects.filter(email=email).first()
        if item is None:
            item = VerificationCode(email=email)
        else:
            time_diff = datetime.datetime.now() - item.last_updated

            if time_diff.total_seconds() < 60 and item.is_last_mail_successful:
                return False, "一分钟之内只能发送一条验证码"

        code = random.randint(1000, 9999)
        item.code = code

        message = """
        尊敬的用户您好！\n\n
        您的验证码为：{0}\n\n\n\n
        注意：此操作可能会修改您的密码。如非本人操作，请及时登录并修改密码以保证帐户安全 \n
        """

        try:
            send_mail(
                subject="Memorest 验证码",
                from_email="memorest@email.streack.cn",
                message="您的验证码为：" + str(code),
                recipient_list=(
                    email,
                ),
                fail_silently=False,
            )
            item.is_last_mail_successful = True
            item.save()
        except SMTPException as e:
            item.is_last_mail_successful = False
            item.save()
            return False, str(e)

        return True, ""
