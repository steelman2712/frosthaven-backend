from django.urls import path

from .views import CharactersView, CharacterView, CardsView, PerksView, CardUnlockView, ItemsView, CharacterItemsView

urlpatterns = [
    path('characters',CharactersView.as_view(), name='characters'),
    path('character/<int:character_id>', CharacterView.as_view(), name='character'),
    path('character', CharacterView.as_view(), name='character'),
    path('cards', CardsView.as_view(), name='cards'),
    path('cards/unlock', CardUnlockView.as_view(), name='cards'),
    path('perks', PerksView.as_view(), name='perks'),
    path("items",ItemsView.as_view(),name="items"),
    path("characteritems",CharacterItemsView.as_view(), name="character_items")
]