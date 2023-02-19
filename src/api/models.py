from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from .constants import get_level

import os

# Create your models here.
class CharacterClass(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    hand_size = models.IntegerField()

    def __str__(self):
        return self.name

class AbilityCard(models.Model):
    name = models.CharField(max_length=200)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)
    initiative = models.IntegerField()
    can_install = models.BooleanField(default=False)
    installation_charges = models.IntegerField(default=1)
    burn_after_install = models.BooleanField(default=False)
    level = models.IntegerField()
    image = models.ImageField(upload_to='cards/', null=True)

    def file(self) -> str:
        return f"https://{os.environ.get('DOMAIN')}/{os.environ.get('SUBDIRECTORY')}/media/{self.image}"
    
    def __str__(self):
        return f"{self.character_class}:{self.name}"

    def payload(self):
        return {
            "id": self.id,
            "name":self.name,
            "initiative":self.initiative,
            "canInstall":self.can_install,
            "installationCharges":self.installation_charges,
            "burnAfterInstall":self.burn_after_install,
            "level":self.level,
            "file":f"https://{os.environ.get('DOMAIN')}/{os.environ.get('SUBDIRECTORY')}/media/{self.image}"
        }

class Item(models.Model):
    name = models.CharField(max_length=200)
    
    description = models.CharField(max_length=500)
    isPassive = models.BooleanField(default=False)
    isFlippable = models.BooleanField(default=False)
    slot = models.CharField(max_length=200)
    uses = models.IntegerField(blank=True, null=True)
    isReturnedOnLongRest = models.BooleanField(default=False)
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    flipName = models.CharField(max_length=200,blank=True, null=True)
    flipDescription = models.CharField(max_length=500, blank=True, null=True)
    flippedUses = models.IntegerField(blank=True, null=True)
    flippedImage = models.ImageField(upload_to='items/', blank=True, null=True)
    flipTimer = models.IntegerField(blank=True, null=True)
    flippedFlipTimer = models.IntegerField(blank=True, null=True)

    upgradedFrom = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.name
    
    def file(self, image) -> str:
        return f"https://{os.environ.get('DOMAIN')}/{os.environ.get('SUBDIRECTORY')}/media/{image}"



    def payload(self):
        item_dict= model_to_dict(self)
        item_dict["itemId"] = item_dict.pop("id")
        for field in item_dict.keys():
            if field.lower().endswith("image"):
                if not item_dict[field]:
                    item_dict[field]=""
                else:
                    item_dict[field] = self.file(item_dict[field])
        return item_dict



class Perk(models.Model):
    name = models.CharField(max_length=200)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='perks/', null=True)
    active = models.BooleanField(default=False)
    max_uses = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.character_class} : {self.name}"

    def payload(self):
        return {
            "id": self.id,
            "name" : self.name,
            "file": f"https://{os.environ.get('DOMAIN')}/{os.environ.get('SUBDIRECTORY')}/media/{self.image}",
            "active":self.active,
            "maxUses":self.max_uses
        }

class Character(models.Model):
    player = models.ForeignKey(User,on_delete=models.CASCADE)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    experience = models.IntegerField(default=0)
    retired = models.BooleanField(default=False)
    notes = models.CharField(max_length=2000, default="")

    gold = models.IntegerField(default=0)
    wood = models.IntegerField(default=0)
    iron = models.IntegerField(default=0)
    leather = models.IntegerField(default=0)

    arrowvine = models.IntegerField(default=0)
    axenut = models.IntegerField(default=0)
    corpsecap = models.IntegerField(default=0)
    flamefruit = models.IntegerField(default=0)
    rockroot = models.IntegerField(default=0)
    snowthistle = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    def basic_info(self):
        return {
            "id":self.id,
            "characterClass":self.character_class.name,
            "name": self.name,
            "retired": self.retired
        }

    def payload(self):
        character_items = self.items.all()
        character_cards = self.cards.all()
        character_perks = self.perks.all()
        items = [character_item.payload() for character_item in character_items]
        ability_cards = [character_card.payload() for character_card in character_cards]
        perks = [character_perk.perk for character_perk in character_perks]
        return {
            "id":self.id,
            "characterClass":self.character_class.name,
            "name": self.name,
            "retired": self.retired,
            "experience":self.experience,
            "level" : get_level(self.experience),
            "handSize":self.character_class.hand_size,
            "notes": self.notes,

            "gold": self.gold,
            "wood":self.wood,
            "iron":self.iron,
            "leather":self.leather,

            "arrowvine": self.arrowvine,
            "axenut": self.axenut,
            "corpsecap": self.corpsecap,
            "flamefruit": self.flamefruit,
            "rockroot": self.rockroot,
            "snowthistle": self.snowthistle,
            
            "items":items,
            "abilityCards":ability_cards,
            "perks":[perk.payload() for perk in perks],
        }

class CharacterCard(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="cards")
    ability_card = models.ForeignKey(AbilityCard, on_delete=models.CASCADE, related_name="character")
    equipped = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['character', 'ability_card'], name='character - card')
        ]

    def __str__(self):
        return f"{self.character} : {self.ability_card}"

    def payload(self):
        card_info = self.ability_card.payload()
        card_info["equipped"] = self.equipped
        return card_info

class CharacterItem(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    equipped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.character} : {self.item}"



    def payload(self):
        item_info = self.item.payload()
        item_info["equipped"] = self.equipped
        item_info["id"] = self.id
        return item_info


class CharacterPerk(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="perks")
    perk = models.ForeignKey(Perk, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.character} : {self.perk}"
