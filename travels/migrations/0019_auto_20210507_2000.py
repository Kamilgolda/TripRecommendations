# Generated by Django 3.1.7 on 2021-05-07 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0018_auto_20210506_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripreservation',
            name='all_inclusive',
            field=models.BooleanField(default=0, verbose_name='All inclusive'),
        ),
        migrations.AddField(
            model_name='tripreservation',
            name='date',
            field=models.ForeignKey(default=111, on_delete=django.db.models.deletion.PROTECT, to='travels.tripdates', verbose_name='Wybierz termin'),
            preserve_default=False,
        ),
    ]
