# Generated by Django 5.0.2 on 2024-02-29 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='shipment_id',
            field=models.IntegerField(null=True),
        ),
    ]