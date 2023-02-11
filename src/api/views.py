from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Character, AbilityCard, Perk, CharacterClass

import json


class CharactersView(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self, request):
        characters = request.user.character_set.all()
        payload = {"characters" : [character.basic_info() for character in characters]}
        return JsonResponse(payload)



class CharacterView(APIView):
    permission_classes=[IsAuthenticated] 
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
            character = Character(player=player, name=name, character_class=character_class)
            character.save()
            return JsonResponse(character.payload())

class CardsView(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self, request):
        character_class_id = request.GET.get("characterClass")
        cards = AbilityCard.objects.filter(character_class=character_class_id)
        payload = {"cards" : [card.payload() for card in cards]}
        return JsonResponse(payload)

class PerksView(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self, request):
        character_class_id = request.GET.get("characterClass")
        perks = Perk.objects.filter(character_class=character_class_id)
        payload = {"perks" : [perk.payload() for perk in perks]}
        return JsonResponse(payload)