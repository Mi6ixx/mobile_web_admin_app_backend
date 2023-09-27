# Generated by Django 4.2.4 on 2023-09-26 23:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100, null=True)),
                ('year_of_admission', models.CharField(max_length=10, null=True)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'male'), ('FEMALE', 'female')], max_length=20,
                                            null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
