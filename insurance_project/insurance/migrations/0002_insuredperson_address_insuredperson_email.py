# Generated by Django 5.0.7 on 2024-08-12 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuredperson',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Adresa'),
        ),
        migrations.AddField(
            model_name='insuredperson',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
    ]
