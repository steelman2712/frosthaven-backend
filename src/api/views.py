from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Character

import json


class CharactersView(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self, request):
        print("Hello")
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
        
            
    def post(self,request):
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            content = body['content']
            character_class = content["character_class"]
            print(character_class)