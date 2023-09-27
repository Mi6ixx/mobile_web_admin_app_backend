# Generated by Django 4.2.4 on 2023-09-27 01:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_student_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='year_of_admission',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)]),
        ),
    ]