# Generated by Django 4.2.15 on 2024-08-28 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0002_user_created_at_user_watchlist_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.TextField(unique=True),
        ),
    ]
