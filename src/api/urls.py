from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('characters',views.characters, name='characters'),
    path('character/<character_id>', views.character, name='character'),
]