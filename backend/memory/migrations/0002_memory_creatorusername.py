# Generated by Django 2.2.10 on 2020-04-26 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memory',
            name='creatorUsername',
            field=models.CharField(default='', max_length=256, verbose_name='创建人用户名'),
            preserve_default=False,
        ),
    ]