# Generated by Django 4.2.4 on 2023-09-26 23:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.IntegerField(max_length=4, null=True),
        ),
    ]
