from rest_framework import serializers

from .models import Character, AbilityCard, Perk, CharacterClass, CharacterCard, Item, CharacterItem



class CharacterClassSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass
        fields = "__all__"

class ItemSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class CharacterItem(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    class Meta:
        model = CharacterItem
        fields = "__all__"

class AbilityCardSerialiser(serializers.ModelSerializer):
    characterClass = serializers.CharField(source='character_class')
    canInstall = serializers.BooleanField(source='can_install')
    installationCharges = serializers.IntegerField(source='installation_charges')
    burnAfterInstall = serializers.BooleanField(source='burn_after_install')


    class Meta:
        model = AbilityCard
        fields = ("id","name","characterClass","initiative","canInstall","installationCharges","burnAfterInstall","level","file")
        read_only_fields = ['account_name']


class CharacterSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Character
        fields = ("payload",)



class CharacterSerialiserMini(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ("id","characterClass","name","retired")


class CharacterCardSerialiser(serializers.ModelSerializer):
    abilityCard = serializers.PrimaryKeyRelatedField(queryset=AbilityCard.objects.all(), source="ability_card")
    class Meta:
        model = CharacterCard
        fields = ["character","abilityCard","equipped"]



class CharacterCardUnlockSerialiser(serializers.ModelSerializer):
    abilityCard = serializers.PrimaryKeyRelatedField(queryset=AbilityCard.objects.all(), source="ability_card")
    class Meta:
        model = CharacterCard
        fields = ("character", "abilityCard")


