# Generated by Django 5.0.7 on 2024-09-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0011_insuredperson_id_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuredperson',
            name='id_number',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='Rodné číslo'),
        ),
    ]
