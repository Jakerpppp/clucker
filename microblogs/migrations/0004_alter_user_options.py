# Generated by Django 4.2.6 on 2023-11-30 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microblogs', '0003_user_followers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['last_name', 'first_name']},
        ),
    ]
