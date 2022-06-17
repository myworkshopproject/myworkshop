import json

from django.http import HttpResponse

from notes.models.block import Block

def get_blocks(request):
    #Création du l'objet JSON à renvoyé à EditorJS
    data={"time":"", "version":'2.24.3', "blocks":[]}
    if not Block.objects.exists():
        data["blocks"].append({"type":"paragraph", "data":{"text":""}, "id":"TheFirst"})
    else:
        for block in Block.objects.order_by("pos"):
            data["blocks"].append({"type":block.type, "data":block.data, "id":block.id})
    
    #Renvoi de la réponse
    return HttpResponse(json.dumps(data))