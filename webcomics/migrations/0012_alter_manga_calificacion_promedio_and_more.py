# Generated by Django 5.0.6 on 2024-06-01 01:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcomics', '0011_alter_manga_type_of_manga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='calificacion_promedio',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='manga',
            name='front_page',
            field=models.ImageField(blank=True, upload_to='portadas/', verbose_name='portada'),
        ),
    ]
