from rest_framework import serializers
from .models import *
from .ext_function import *


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSave
        fields = ('id', 'name', 'url', 'picture', 'width', 'height', 'parent_picture')

        # This will handle rename

    def create(self, validated_data):
        #
        # if self.data.__getitem__('url') and self.context['request'].FILES:
        #     return
        print(self)
        print(self.data)
        if self.data.__getitem__('url') or self.context['request'].FILES:
            all_data = create_img_url(self.data.__getitem__('url'), self.context['request'].FILES)
            validated_data.update(all_data)
            print(f'Это validated_data перед записью в базу: {validated_data}')

            return ImageSave.objects.create(**validated_data)

        # validated_data.update({'picture': self.context['request'].FILES['file']})
        return ImageSave.objects.create(**validated_data)


class ImagesSerializerResize(serializers.ModelSerializer):
    class Meta:
        model = ImageSave
        fields = ('id', 'name', 'url', 'picture', 'width', 'height', 'parent_picture')
    # id = serializers.IntegerField(label='ID', read_only=True)
    # name = serializers.CharField(allow_blank=True, label='Имя', max_length=200, required=False)
    # url = serializers.URLField(allow_blank=True, allow_null=True, label='URL  изображения', max_length=200,
    #                            required=False)
    # picture = serializers.ImageField(label='Изображение', max_length=100, required=False)
    # width = serializers.IntegerField(allow_null=True, label='Ширина', required=False)
    # height = serializers.IntegerField(allow_null=True, label='Высота', required=False)
    # parent_picture = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=ImageSave.objects.all(),
    #                                                     required=False)
    #
    # def update(self, instance, validated_data):
    #     print(f'This Self: {self}')
    #     print(f'This INSTANS: {instance}')
    #     print(f'This validated_data: {validated_data}')
    #
    #     instance.width = validated_data.get('title', instance.width)
    #     # instance.description = validated_data.get('description', instance.description)
    #     # instance.body = validated_data.get('body', instance.body)
    #     # instance.author_id = validated_data.get('author_id', instance.author_id)
    #     instance.save()
    #     return instance
