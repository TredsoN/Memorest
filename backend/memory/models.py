from django.db import models


# Create your models here.
class Memory(models.Model):
    privacy_choices = (
        (0, '私密记忆'),
        (1, '公开记忆')
    )

    creatorId = models.IntegerField(verbose_name='创建人编号')
    creatorUsername = models.CharField(max_length=256, verbose_name='创建人用户名')
    subjectId = models.IntegerField(blank=True, null=True, verbose_name='记忆主题编号')
    subjectName = models.CharField(max_length=256, verbose_name='记忆主题名称')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    title = models.CharField(max_length=256, verbose_name='记忆标题')
    picture = models.CharField(max_length=256, blank=True, null=True, verbose_name='图片文件地址')
    audio = models.CharField(max_length=256, blank=True, null=True, verbose_name='音频文件地址')
    content = models.CharField(max_length=256, verbose_name='记忆内容')
    visitor = models.IntegerField(default=0, verbose_name='访问量')
    privacy = models.IntegerField(default=0, verbose_name='私密/公开记忆')
    activity = models.IntegerField(default=100, verbose_name='活性')
    recallTime = models.IntegerField(default=0, verbose_name='回忆的次数')
    deathtime = models.IntegerField(default=0, verbose_name='记忆死亡天数')

    class Meta:
        db_table = 'memory'
        verbose_name = '记忆'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class Subject(models.Model):

    name = models.CharField(max_length=256, verbose_name='主题')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'subject'
        verbose_name = '主题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class News(models.Model):

    title = models.CharField(max_length=256, verbose_name='咨讯标题')
    summary = models.TextField(verbose_name='咨讯摘要')
    content = models.TextField(verbose_name='咨讯内容')
    author = models.CharField(max_length=256, verbose_name='咨讯作者')
    origin = models.CharField(max_length=256, verbose_name='咨讯来源')
    time = models.DateTimeField(verbose_name='咨讯时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'news'
        verbose_name = '咨讯'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(verbose_name="图片", upload_to="image")
    memoryid = models.IntegerField(verbose_name='记忆编号')


class Music(models.Model):
    music = models.FileField(verbose_name="音乐", upload_to="music")
    memoryid = models.IntegerField(verbose_name='记忆编号')