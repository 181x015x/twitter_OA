# Generated by Django 2.0.6 on 2018-06-27 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_auto_20180628_0202'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='total_point',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]