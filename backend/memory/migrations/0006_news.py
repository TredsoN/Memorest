# Generated by Django 2.2.10 on 2020-05-01 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0005_auto_20200426_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='咨询标题')),
                ('content', models.CharField(max_length=256, verbose_name='咨询内容')),
                ('picture', models.CharField(max_length=256, verbose_name='咨询图片')),
                ('origin', models.CharField(max_length=256, verbose_name='咨询来源')),
                ('time', models.DateTimeField(verbose_name='咨询时间')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '咨询',
                'verbose_name_plural': '咨询',
                'db_table': 'news',
            },
        ),
    ]