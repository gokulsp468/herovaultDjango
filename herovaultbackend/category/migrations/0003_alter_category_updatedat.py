# Generated by Django 4.2.13 on 2024-05-13 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_alter_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
