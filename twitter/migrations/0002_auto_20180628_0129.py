# Generated by Django 2.0.6 on 2018-06-27 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='oauth_token',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
