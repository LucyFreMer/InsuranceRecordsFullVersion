# Generated by Django 5.0.7 on 2024-08-25 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0008_remove_insurancetype_coverage_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='coverage_amount',
        ),
    ]
