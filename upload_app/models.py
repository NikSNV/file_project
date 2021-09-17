from django.db import models


class ImageSave(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя", blank=True)
    url = models.URLField(verbose_name="URL  изображения", null=True, blank=True)
    picture = models.ImageField(upload_to='', verbose_name="Изображение", height_field='height', width_field='width', blank=True)
    width = models.PositiveIntegerField(blank=True, null=True, verbose_name="Ширина")
    height = models.PositiveIntegerField(blank=True, null=True, verbose_name="Высота")
    parent_picture = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
