# Generated by Django 2.2.16 on 2020-11-14 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drifter', '0003_drifter_ocean'),
    ]

    operations = [
        migrations.AddField(
            model_name='drifter_user',
            name='state',
            field=models.CharField(max_length=4, null=True, verbose_name='登陆状态'),
        ),
    ]
