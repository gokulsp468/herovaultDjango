# Generated by Django 4.2.13 on 2024-05-13 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='created_at',
            new_name='createdAt',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='updated_at',
            new_name='updatedAt',
        ),
    ]
