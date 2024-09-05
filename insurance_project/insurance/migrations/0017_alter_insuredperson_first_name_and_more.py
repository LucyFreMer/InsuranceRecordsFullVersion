# Generated by Django 5.0.7 on 2024-09-02 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0016_alter_insuredperson_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuredperson',
            name='first_name',
            field=models.CharField(max_length=20, verbose_name='Jméno'),
        ),
        migrations.AlterField(
            model_name='insuredperson',
            name='last_name',
            field=models.CharField(max_length=20, verbose_name='Příjmení'),
        ),
    ]