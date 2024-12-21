# Generated by Django 4.2.17 on 2024-12-19 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(blank=True, choices=[('TR', 'Transmitter'), ('AL', 'Analyser'), ('PG', 'Pressure Gauge'), ('VV', 'Valves'), ('PS', 'Postioners')], max_length=2, null=True)),
                ('image', models.ImageField(upload_to='media/')),
            ],
        ),
    ]