from django.urls import path
from . import views

app_name = 'music_converter'

urlpatterns = [
    path('', views.index, name='index')
]
