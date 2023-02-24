from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework.parsers import JSONParser


import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes

from .models import Character, AbilityCard, Perk, CharacterClass, CharacterCard, Item, CharacterItem, CharacterPerk
from .serialisers import CharacterSerialiser, CharacterCardSerialiser, AbilityCardSerialiser, CharacterCardUnlockSerialiser, CharacterSerialiserMini, CharacterSerialiser, ItemSerialiser

import json


class CharactersView(APIView):
    permission_classes=[IsAuthenticated] 
    serializer_class = CharacterSerialiserMini(many=True)

    def get(self, request):
        characters = request.user.character_set.all()
        #payload = {"characters" : [character.basic_info() for character in characters]}
        payload = CharacterSerialiserMini(characters, many=True)
        return Response(payload.data)

class CharacterView(APIView):
    permission_classes=[IsAuthenticated] 
    serializer_class = CharacterSerialiser
    def get(self, request, character_id):
        try:
            character = Character.objects.get(id=character_id)
            return JsonResponse(character.payload())
        except Character.DoesNotExist:
             raise Http404
        

    def patch(self, request):
        body = json.loads(request.body.decode('utf-8'))
        character_id = body["characterId"]
        character = Character.objects.get(id=character_id)
        for key in body.keys():
            if key != "characterId":
                setattr(character,key,body[key])
        character.save()
        return HttpResponse(status=204)


    def post(self,request):
            player = request.user
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            character_class_name = body["characterClass"]
            name = body["name"]
            character_class = CharacterClass.objects.filter(name=character_class_name).all()[0]
            character = Character(player=player, name=name, characterClass=character_class)
            character.save()

            cards = AbilityCard.objects.filter(character_class=character_class, level=1).all()
            hand_size = character_class.hand_size
            i = 0
            for card in cards:
                if i < hand_size:
                    character_card = CharacterCard(character=character,ability_card=card,equipped=True)
                else:
                    character_card = CharacterCard(character=character,ability_card=card,equipped=False)
                character_card.save()
                i = i + 1

            return JsonResponse(character.payload())

class CardsView(APIView):
    permission_classes=[IsAuthenticated] 
    

    @extend_schema(parameters=[
        OpenApiParameter("characterClass", OpenApiTypes.STR)
    ],        
        responses=AbilityCardSerialiser(many=True))
    def get(self, request):
        self.serializer_class = AbilityCardSerialiser
        character_class = request.GET.get("characterClass")
        cards = AbilityCard.objects.filter(character_class=character_class)
        serialiser = AbilityCardSerialiser(cards, many=True)
        payload = serialiser.data
        return JsonResponse(payload, safe=False)
    
    @extend_schema(request=CharacterCardSerialiser(many=True))
    def post(self, request):
        self.serializer_class = CharacterCardSerialiser
        data = JSONParser().parse(request)
        serialiser = CharacterCardSerialiser(data=data, many=True)
        for card in data:
            CharacterCard.objects.filter(character=card["character"],ability_card=card["abilityCard"]).all().delete()
        if serialiser.is_valid():
            serialiser.save()
            return JsonResponse(serialiser.data, status=201, safe=False)
        return Response(serialiser.errors, status=400)

class ItemsView(APIView):
    permission_classes=[IsAuthenticated] 

    @extend_schema(responses=ItemSerialiser(many=True))
    def get(self, request):
        items = Item.objects.all()
        payload = [item.payload() for item in items]
        return JsonResponse(payload, safe=False)
    
    
class CharacterItemsView(APIView):
    permission_classes=[IsAuthenticated] 

    def patch(self, request):
        data = JSONParser().parse(request)
        items = CharacterItem.objects.filter(character=data["characterId"]).all()
        for item in items:
            if item.id in data["itemsToEquip"]:
                item.equipped = True
            else:
                item.equipped = False
            item.save(update_fields=["equipped"])
        return HttpResponse(status=200)


    def post(self, request):
        data = JSONParser().parse(request)
        character = Character.objects.filter(id=data["characterId"]).first()
        item = Item.objects.filter(id=data["itemId"]).first()
        character_item = CharacterItem(character=character,item=item,equipped=False)
        character_item.save()
        return JsonResponse(data=character_item.payload(),status=200)
    
    def delete(self, request):
        data = JSONParser().parse(request)
        character_item = CharacterItem.objects.filter(id=data["characterItemId"]).first()
        character_item.delete()
        return HttpResponse(status=200)


class CardUnlockView(APIView):
    serializer_class = CharacterCardUnlockSerialiser
    @extend_schema(request=CharacterCardUnlockSerialiser(many=False))
    def post(self, request):
        data = JSONParser().parse(request)
        serialiser = CharacterCardUnlockSerialiser(data=data, many=False)
        if serialiser.is_valid():
            serialiser.save()
            return JsonResponse(serialiser.data, status=201)
        return JsonResponse(serialiser.errors, status=400)

class PerksView(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self, request):
        character_class_id = request.GET.get("characterClass")
        perks = Perk.objects.filter(character_class=character_class_id)
        payload = {"perks" : [perk.payload() for perk in perks]}
        return JsonResponse(payload)
    
    def post(self, request):
        data = JSONParser().parse(request)
        character = Character.objects.filter(id=data["characterId"]).first()
        if not character:
            return HttpResponse("Invalid character id",status=400)
        perk = Perk.objects.filter(id=data["perkId"]).first()
        if not perk:
            return HttpResponse("Invalid perk id",status=400)
        character_perk = CharacterPerk(character = character, perk=perk)
        character_perk.save()
        return HttpResponse(status=200)

