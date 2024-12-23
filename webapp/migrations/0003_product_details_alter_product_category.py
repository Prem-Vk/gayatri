# Generated by Django 4.2.17 on 2024-12-21 07:52

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='details',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('TR', 'Transmitter'), ('AL', 'Analyser'), ('PG', 'Pressure Gauge'), ('VV', 'Valves'), ('PS', 'Postioners'), ('PT', 'Pipe Tube'), ('FT', 'Fittings'), ('SG', 'Switchgears'), ('PM', 'Pumps'), ('MR', 'Motors'), ('FA', 'Fans'), ('WS', 'Weilding Spares'), ('TS', 'Tools and Spares'), ('EC', 'Encoder'), ('CP', 'Coupling'), ('GX', 'GearBoxes'), ('LI', 'Lab Instrument'), ('HP', 'Hose Pipe')], max_length=2, null=True),
        ),
    ]
