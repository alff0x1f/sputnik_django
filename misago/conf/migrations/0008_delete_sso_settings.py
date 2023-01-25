# Generated by Django 3.2.15 on 2023-01-04 12:37

from django.db import migrations

settings = (
    "enable_sso",
    "sso_public_key",
    "sso_private_key",
    "sso_url",
)


def delete_sso_settings(apps, _):
    Setting = apps.get_model("misago_conf", "Setting")
    Setting.objects.filter(setting__in=settings).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("misago_conf", "0007_add_oauth2_settings"),
    ]

    operations = [migrations.RunPython(delete_sso_settings)]