# Generated by Django 3.2.23 on 2024-04-28 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_rename_signup_signupmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=256)),
            ],
        ),
        migrations.DeleteModel(
            name='SignupModel',
        ),
    ]
