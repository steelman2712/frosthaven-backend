from django.contrib import admin
from .models import CharacterClass,AbilityCard,Item,Character,CharacterCard,CharacterItem,Perk,CharacterPerk

admin.site.register(CharacterClass)
admin.site.register(AbilityCard)
admin.site.register(Item)
admin.site.register(Perk)
admin.site.register(Character)
admin.site.register(CharacterCard)
admin.site.register(CharacterItem)
admin.site.register(CharacterPerk)

# Register your models here.
