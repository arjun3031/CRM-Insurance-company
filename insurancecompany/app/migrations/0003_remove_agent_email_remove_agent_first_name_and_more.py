# Generated by Django 5.1.3 on 2024-11-13 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_agent_email_alter_agent_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='email',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='last_name',
        ),
    ]
