# Generated by Django 5.1.2 on 2024-10-25 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('residents_management', '0002_alter_room_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='building',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='resident',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['building', 'number']},
        ),
    ]