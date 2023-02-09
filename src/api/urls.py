from django.urls import path

from .views import CharactersView, CharacterView

urlpatterns = [
    path('characters',CharactersView.as_view(), name='characters'),
    path('character/<character_id>', CharacterView.as_view(), name='character'),
]