# Generated by Django 5.1.2 on 2024-10-25 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('residents_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('number', 'building')},
        ),
    ]
