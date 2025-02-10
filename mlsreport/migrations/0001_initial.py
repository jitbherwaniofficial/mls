# Generated by Django 5.1.4 on 2025-02-08 10:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicNeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('zone', models.CharField(choices=[('west zone', 'West Zone'), ('south zone', 'South Zone'), ('east zone', 'East Zone'), ('north zone', 'North Zone'), ('municiple', 'Municipal'), ('private', 'Private'), ('unknown', 'Unknown'), ('sewers', 'Sewers')], max_length=20)),
                ('icon', models.FileField(blank=True, null=True, upload_to='basic_needs_icons/')),
            ],
        ),
        migrations.CreateModel(
            name='MLSReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_image', models.FileField(blank=True, null=True, upload_to='property_images/')),
                ('property_address', models.CharField(max_length=255)),
                ('tag', models.CharField(choices=[('new', 'New'), ('old', 'Old')], max_length=5)),
                ('postal_code_address', models.CharField(max_length=100)),
                ('taxes', models.CharField(blank=True, max_length=10, null=True)),
                ('taxes_year', models.IntegerField()),
                ('lot_plan', models.CharField(blank=True, max_length=100, null=True)),
                ('spis', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=5)),
                ('no_of_rooms', models.CharField(blank=True, max_length=5, null=True)),
                ('bedrooms', models.CharField(max_length=5)),
                ('washrooms', models.CharField(max_length=5)),
                ('parkings', models.CharField(max_length=5)),
                ('detached', models.CharField(choices=[('detached', 'Detached'), ('undetached', 'Undetached')], max_length=20)),
                ('link', models.CharField(choices=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')], max_length=10)),
                ('front_on', models.CharField(choices=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')], max_length=10)),
                ('acre', models.CharField(blank=True, max_length=20, null=True)),
                ('dir_cross_st', models.CharField(blank=True, max_length=255, null=True)),
                ('irreg', models.CharField(max_length=100)),
                ('client_desc', models.TextField()),
                ('extras', models.TextField()),
                ('mls_number', models.CharField(max_length=10)),
                ('holdover', models.IntegerField()),
                ('pin_number', models.CharField(max_length=8)),
                ('possession_remarks', models.CharField(max_length=10)),
                ('arn_number', models.CharField(max_length=8)),
                ('occupancy', models.CharField(max_length=10)),
                ('contact_after_expiry', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1)),
                ('kitchens', models.CharField(max_length=20)),
                ('family_room', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=5)),
                ('basement', models.CharField(max_length=20)),
                ('fireplace_stv', models.CharField(max_length=20)),
                ('heat', models.CharField(max_length=20)),
                ('air_conditioning', models.CharField(max_length=20)),
                ('central_vac', models.CharField(max_length=20)),
                ('approximate_age', models.CharField(max_length=20)),
                ('approximate_sqft', models.CharField(max_length=20)),
                ('assesment', models.CharField(max_length=20)),
                ('potl', models.CharField(max_length=20)),
                ('elevator_lift', models.CharField(max_length=20)),
                ('laundry_lev', models.CharField(max_length=20)),
                ('physical_hdcp_eqp', models.CharField(max_length=20)),
                ('exterior', models.CharField(max_length=20)),
                ('drive', models.CharField(max_length=20)),
                ('garage_parking_space', models.CharField(max_length=20)),
                ('total_parkings', models.CharField(max_length=20)),
                ('uffi', models.CharField(max_length=20)),
                ('pool', models.CharField(max_length=20)),
                ('energy_certificate', models.CharField(max_length=20)),
                ('certificate_level', models.CharField(blank=True, max_length=20, null=True)),
                ('green_pis', models.CharField(max_length=20)),
                ('prop_feat', models.CharField(max_length=20)),
                ('basic_needs', models.ManyToManyField(to='mlsreport.basicneed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_title', models.CharField(max_length=100)),
                ('room_level', models.CharField(choices=[('main', 'Main'), ('second', 'Second'), ('basement', 'Basement')], max_length=20)),
                ('room_length', models.DecimalField(decimal_places=2, max_digits=5)),
                ('room_width', models.DecimalField(decimal_places=2, max_digits=5)),
                ('room_description', models.TextField()),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='mlsreport.mlsreport')),
            ],
        ),
    ]
