# Generated by Django 5.0.6 on 2024-06-22 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcomics', '0020_alter_manga_type_of_manga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='front_page',
            field=models.ImageField(blank=True, db_column='portadas', upload_to='webcomics/static/images/front_pages/', verbose_name='portada'),
        ),
    ]
