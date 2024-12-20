# Generated by Django 5.1.3 on 2024-11-22 05:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_client_campaign'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(max_length=10, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('profession', models.CharField(blank=True, max_length=100, null=True)),
                ('annual_income', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('qualification', models.CharField(blank=True, max_length=100, null=True)),
                ('aadhar', models.CharField(blank=True, max_length=12, null=True)),
                ('pan', models.CharField(blank=True, max_length=10, null=True)),
                ('income_level', models.CharField(blank=True, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=10, null=True)),
                ('children', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True)),
                ('source', models.JSONField(blank=True, null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('claim_satisfaction', models.IntegerField(blank=True, null=True)),
                ('insurance_area', models.JSONField(blank=True, null=True)),
                ('agent_visited_policy', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('willingness_to_purchase', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True)),
                ('willingness_to_share_previous_insurance', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True)),
                ('customer_preferences', models.TextField(blank=True, null=True)),
                ('agent_notes', models.TextField(blank=True, null=True)),
                ('willingness_to_switch', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True)),
                ('existing_profile_details', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaign_clients', to='app.agent')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaign_clients', to='app.campaign')),
            ],
        ),
    ]
