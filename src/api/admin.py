from django.contrib import admin
from .models import CharacterClass,AbilityCard,Item,Character,CharacterCard,CharacterItem

admin.site.register(CharacterClass)
admin.site.register(AbilityCard)
admin.site.register(Item)
admin.site.register(Character)
admin.site.register(CharacterCard)
admin.site.register(CharacterItem)

# Register your models here.
