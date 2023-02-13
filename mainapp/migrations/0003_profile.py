# Generated by Django 2.2.24 on 2023-01-23 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_delete_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(default='匿名ユーザ', max_length=30)),
                ('zipcode', models.CharField(default='', max_length=8)),
                ('prefecture', models.CharField(default='', max_length=6)),
                ('city', models.CharField(default='', max_length=100)),
                ('address1', models.CharField(default='', max_length=200)),
                ('address2', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
