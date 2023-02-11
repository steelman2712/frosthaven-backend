from django.urls import path

from .views import CharactersView, CharacterView, CardsView, PerksView

urlpatterns = [
    path('characters',CharactersView.as_view(), name='characters'),
    path('character/<character_id>', CharacterView.as_view(), name='character'),
    path('character', CharacterView.as_view(), name='character'),
    path('cards', CardsView.as_view(), name='cards'),
    path('perks', CardsView.as_view(), name='cards'),
]