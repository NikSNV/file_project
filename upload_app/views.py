import os

from django.core.files import File
from django.shortcuts import render, get_object_or_404
from requests import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from .forms import ImageForm
from .models import *

from PIL import Image

from django.conf import settings

from .serializers import *

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView


def image_upload_view(request):
    """ Загрузка файлов пользователем и обработка"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if not request.FILES and not request.POST['url']:
            form.add_error(None, 'Выберите файл или заполните URL файла!')
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            img_obj = form.instance
            return render(request, 'upload_app/index.html', {'form': form, 'img_obj': img_obj})
        else:
            form.add_error(None, 'Ошибка валидности')
    else:
        form = ImageForm()

    return render(request, 'upload_app/index.html', {'form': form})


def resize_image(request):
    """Модуль изменения размеро файла"""

    # Берем последнюю запись из базы
    img = ImageSave.objects.last()
    image_field_path = img.picture

    # Добавляем НОЛЬ к имени файла и выделяем имя файла из пути
    name_img_str = str(image_field_path)
    nom_toski = name_img_str.rfind('.')
    # Новое имя файла и путь
    new_str_patch_image = name_img_str[:nom_toski] + '_0' + name_img_str[nom_toski:]
    new_str_patch_image_short = name_img_str[:nom_toski] + '_0' + name_img_str[nom_toski:]

    # Имя файла без пути
    nom_slesh = name_img_str.rfind('/')
    str_file = name_img_str[nom_slesh + 1:]
    # Создаем новое имя файла
    nom_toski = str_file.rfind('.')
    new_str_file = str_file[:nom_toski] + '_0' + str_file[nom_toski:]

    print(f'Текущий путь {image_field_path}')

    print(f'Новый путь {new_str_patch_image}')
    print(new_str_file)
    print("Текущая деректория:", os.getcwd())
    print(settings.MEDIA_ROOT)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if not request.POST['width'] or not request.POST['height']:
            form.add_error(None, 'Выберите ширину и высоту!')
            return render(request, 'upload_app/resize.html', {'form': form, 'img_obj': img})
        else:
            new_width = int(request.POST['width'])
            new_height = int(request.POST['height'])
            # Открываем исходник для resize и пересохранения под другим именем
            f = Image.open(image_field_path)
            f = f.resize((new_width, new_height), Image.ANTIALIAS)
            f.save(new_str_patch_image)
            # f.show()
            new_file = File(open(new_str_file, "rb"))
            img_obj = ImageSave.objects.create(name=new_str_file, url=img.url, picture=new_file, width=new_width,
                                               height=new_width, parent_picture=img)
            # Уберем мусор за собой
            new_file.close()
            os.remove(new_str_file)
            return render(request, 'upload_app/resize.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'upload_app/resize.html', {'form': form, 'img_obj': img})


class ImagesView(ListCreateAPIView):
    queryset = ImageSave.objects.all()
    serializer_class = ImagesSerializer


class SingleImageView(RetrieveUpdateDestroyAPIView):
    queryset = ImageSave.objects.all()
    serializer_class = ImagesSerializer


class SingleImageViewResize(RetrieveUpdateDestroyAPIView):
    queryset = ImageSave.objects.all()
    serializer_class = ImagesSerializerResize
    # def put(self, request, pk):
    #     saved_article = get_object_or_404(ImageSave.objects.all(), pk=pk)
    #     data = request.data.get('width')
    #     serializer = ImagesSerializerResize(instance=saved_article, data=data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         article_saved = serializer.save()
    #     return Response({
    #         "success": "Article '{}' updated successfully".format(article_saved.title)
    #     })

    def put(self, instance, **validated_data):
        print(f'ЭТО ОБНОВЛЕНИЕ!! {validated_data}')
        print(f'ЭТО instance!! {instance.data}')
        print(f'ЭТО self!! {self.get_object()}')

        # instance.name = validated_data['name']
        return Response(ImagesSerializerResize.data)
