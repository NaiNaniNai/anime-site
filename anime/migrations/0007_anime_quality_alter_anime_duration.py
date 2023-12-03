# Generated by Django 4.2.6 on 2023-12-03 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("anime", "0006_anime_duration"),
    ]

    operations = [
        migrations.AddField(
            model_name="anime",
            name="quality",
            field=models.CharField(
                choices=[
                    ("FHD", "Full High Definition 1080p"),
                    ("HD", "High Definition 720p"),
                    ("HQ", "High Quality 480p"),
                    ("SD", "Standard definition 360p"),
                    ("Пока не объявлено", "Пока неизвестно"),
                ],
                default="Пока не объявлено",
                max_length=128,
                verbose_name="Качество",
            ),
        ),
        migrations.AlterField(
            model_name="anime",
            name="duration",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Длительность в минутах (0, если неизвестно)",
            ),
        ),
    ]
