# Generated by Django 4.2.10 on 2024-02-21 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donations", "0006_remove_job_url_job_date_finished_job_zip"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donor",
            name="date_created",
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="date created"),
        ),
        migrations.AlterField(
            model_name="ngo",
            name="date_created",
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="date created"),
        ),
    ]
