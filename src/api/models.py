from django.db import models
from django.contrib.auth.models import User
from .constants import get_level

# Create your models here.
class CharacterClass(models.Model):
    name = models.CharField(max_length=200)
    hand_size = models.IntegerField()

    def __str__(self):
        return self.name

class AbilityCard(models.Model):
    name = models.CharField(max_length=200)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    initiative = models.IntegerField()
    can_install = models.BooleanField()
    installation_charges = models.IntegerField()
    burn_after_install = models.BooleanField()
    level = models.IntegerField()

    def __str__(self):
        return self.name

    def payload(self):
        return {
            "name":self.name,
            "initiative":self.initiative,
            "can_install":self.can_install,
            "installation_charges":self.installation_charges,
            "burn_after_install":self.burn_after_install,
            "level":self.level
        }

class Item(models.Model):
    name = models.CharField(max_length=200)
    flip_name = models.CharField(max_length=200,blank=True, null=True)
    description = models.CharField(max_length=500)
    flip_description = models.CharField(max_length=500, blank=True, null=True)
    slot = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def payload(self):
        return {
            "id": self.id,
            "name": self.name,
            "flip_name": self.flip_name,
            "description": self.description,
            "flip_description": self.flip_description,
            "slot": self.slot
        }

class Perk(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

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
            "character_class":self.character_class.name,
            "name": self.name,
            "retired": self.retired
        }

    def payload(self):
        character_items = self.characteritem_set.all()
        character_cards = self.charactercard_set.all()
        items = [character_item.item for character_item in character_items]
        ability_cards = [character_card.ability_card for character_card in character_cards]
        return {
            "id":self.id,
            "character_class":self.character_class.name,
            "name": self.name,
            "retired": self.retired,
            "experience":self.experience,
            "level" : get_level(self.experience),
            "hand_size":self.character_class.hand_size,
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
            
            "items":[item.payload() for item in items],
            "ability_cards":[ability_card.payload() for ability_card in ability_cards]
        }

class CharacterCard(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    ability_card = models.ForeignKey(AbilityCard, on_delete=models.CASCADE)
    equipped = models.BooleanField()

    def __str__(self):
        return f"{self.character} : {self.ability_card}"

class CharacterItem(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    equipped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.character} : {self.item}"

class CharacterPerk(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    perk = models.ForeignKey(Perk, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)


    