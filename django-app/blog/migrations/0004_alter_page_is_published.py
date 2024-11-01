# Generated by Django 5.1.2 on 2024-11-01 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='is_published',
            field=models.BooleanField(default=False, help_text='This field must be checked for the page to be displayed'),
        ),
    ]
