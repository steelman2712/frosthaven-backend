from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Character

import json

@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def characters(request):
    characters = request.user.character_set.all()
    payload = {"characters" : [character.basic_info() for character in characters]}
    return JsonResponse(payload)

@login_required
def character(request, character_id):
    if request.method == "GET":
        character = Character.objects.get(id=character_id)
        return JsonResponse(character.payload())
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['content']
        character_class = content["character_class"]
        print(character_class)