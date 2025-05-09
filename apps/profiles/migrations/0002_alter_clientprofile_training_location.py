# Generated by Django 4.2.20 on 2025-04-28 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clientprofile",
            name="training_location",
            field=models.CharField(
                choices=[("gym", "Зал"), ("home", "Дом"), ("outdoors", "Улица")],
                help_text="Preferred training location",
                max_length=50,
            ),
        ),
    ]
