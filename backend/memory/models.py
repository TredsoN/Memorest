from django.db import models


# Create your models here.
class Memory(models.Model):
    category1_choices = (
        (0, '个人记忆'),
        (1, '集体记忆')
    )
    category2_choices = (
        (0, '私密记忆'),
        (1, '公开记忆')
    )

    name = models.CharField(max_length=256, verbose_name='记忆名字')
    creatorId = models.IntegerField(verbose_name='创建人编号')
    subjectId = models.IntegerField(blank=True, null=True, verbose_name='集体记忆编号')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    picture = models.CharField(max_length=256, blank=True, null=True, verbose_name='图片文件地址')
    audio = models.CharField(max_length=256, blank=True, null=True, verbose_name='音频文件地址')
    content = models.CharField(max_length=256, verbose_name='记忆内容')
    visitor = models.IntegerField(default=0, verbose_name='访问量')
    category1 = models.IntegerField(choices=category1_choices, verbose_name='个人/集体记忆')
    category2 = models.IntegerField(choices=category2_choices, verbose_name='私密/公开记忆')
    activity = models.IntegerField(default=100, verbose_name='活性')

    class Meta:
        db_table = 'memory'
        verbose_name = '记忆'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Subject(models.Model):

    name = models.CharField(max_length=256, verbose_name='主题')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'subject'
        verbose_name = '主题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
