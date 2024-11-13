# Generated by Django 5.1.3 on 2024-11-12 18:01

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0002_alter_medication_options_alter_medication_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RefillRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('street', models.CharField(blank=True, max_length=200, null=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refill_requests', to='medications.medication')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='refill_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Refill Request',
                'verbose_name_plural': 'Refill Requests',
                'ordering': ['-created_at'],
            },
        ),
    ]
