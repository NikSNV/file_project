import os

from django import forms
import requests
from django.core.files import File

from .models import *


class ImageForm(forms.ModelForm):

    # Переопределили clean()

    def clean(self, *args, **kwargs):
        all_data = self.cleaned_data
        url = all_data['url']
        image = all_data['picture']
        name = all_data['name']

        if not image and url:
            print('зашли в проверку УРЛЫ')
            img = requests.get(url, stream=True)
            print(img)
            path_file = name + '.jpg'
            img_temp = open(path_file, 'wb')
            img_temp.write(img.content)
            img_temp.close()
            all_data['picture'] = File(open(img_temp.name, "rb"))
            os.remove(img_temp.name)
        return all_data

    # # Валидируем заголовок
    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if len(name) > 200:
    #         raise ValidationError('Длина превышает 200 символов')
    #     if not name:
    #         raise ValidationError('Заголовок обязателен к заполнению!')
    #     return name

    class Meta:
        model = ImageSave
        fields = ['name', 'url', 'picture', 'width', 'height', 'parent_picture']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }
