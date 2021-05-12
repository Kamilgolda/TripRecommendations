# Generated by Django 3.1.7 on 2021-05-11 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0019_auto_20210507_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='city',
            field=models.CharField(blank=True, max_length=50, verbose_name='Miejsce wycieczki'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='climate',
            field=models.CharField(blank=True, choices=[('Górski', 'Górski'), ('Morski', 'Morski'), ('Kontynentalny', 'Kontynentalny'), ('Śródziemnomorski', 'Śródziemnomorski'), ('Monsunowy', 'Monsunowy'), ('Stepowy', 'Stepowy'), ('Pustynny', 'Pustynny')], max_length=20, verbose_name='Klimat'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='countryEN',
            field=models.CharField(blank=True, max_length=50, verbose_name='Kraj wycieczki po angielsku'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='currency',
            field=models.CharField(blank=True, max_length=5, verbose_name='Skrót waluty'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='head_description',
            field=models.TextField(blank=True, max_length=2000, verbose_name='Główny opis'),
        ),
    ]
