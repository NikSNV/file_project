# Generated by Django 3.2.7 on 2021-09-15 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageSave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Имя')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL  изображения')),
                ('picture', models.ImageField(blank=True, height_field='height', upload_to='', verbose_name='Изображение', width_field='width')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Ширина')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='Высота')),
                ('parent_picture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='upload_app.imagesave')),
            ],
        ),
    ]