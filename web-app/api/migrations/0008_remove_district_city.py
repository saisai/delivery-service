# Generated by Django 2.2.15 on 2020-10-01 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200919_0050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='city',
        ),
    ]