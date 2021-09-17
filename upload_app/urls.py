from django.urls import path

from .views import *


urlpatterns = [
    path('images/', ImagesView.as_view()),
    path('images/<int:pk>/', SingleImageView.as_view()),
    path('images/<int:pk>/resize/', SingleImageViewResize.as_view()),

]