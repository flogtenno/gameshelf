# Generated by Django 4.2.2 on 2024-03-14 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('top', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['tag']},
        ),
    ]