# Generated by Django 5.1.3 on 2024-11-21 10:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_campaign_agent_campaign_agents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='agents',
        ),
        migrations.AddField(
            model_name='campaign',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.agent'),
        ),
    ]
