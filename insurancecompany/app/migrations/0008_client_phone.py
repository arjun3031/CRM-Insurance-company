# Generated by Django 5.1.3 on 2024-11-16 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_client_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
