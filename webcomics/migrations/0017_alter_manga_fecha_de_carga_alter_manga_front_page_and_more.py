# Generated by Django 5.0.3 on 2024-06-05 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcomics', '0016_alter_manga_table_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='fecha_de_carga',
            field=models.DateField(db_column='fecha', max_length=100, verbose_name='Fecha de carga'),
        ),
        migrations.AlterField(
            model_name='manga',
            name='front_page',
            field=models.ImageField(blank=True, db_column='portadas', upload_to='portadas/', verbose_name='portada'),
        ),
        migrations.AlterField(
            model_name='manga',
            name='publicado_por',
            field=models.CharField(blank=True, db_column='autor', max_length=100, verbose_name='publicado_por'),
        ),
        migrations.AlterField(
            model_name='manga',
            name='type_of_manga',
            field=models.CharField(blank=True, choices=[('Accion', 'Acción'), ('Aventura', 'Aventura')], db_column='Género del manga', default=('Accion', 'Acción'), help_text='Agregar el género del manga', max_length=10, verbose_name='Género del manga'),
        ),
    ]
