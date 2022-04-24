# Generated by Django 3.1.3 on 2022-04-24 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('superadmin', 'Super Admin'), ('customer', 'Customer')], default='superadmin', max_length=32)),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('settings', models.JSONField(default=dict)),
                ('added_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_added_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='related_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]