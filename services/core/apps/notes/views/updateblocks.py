import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from notes.models.block import Block

@csrf_exempt
def update_blocks(request):
    #récupération des données brutes en dico
    data = json.loads(request.body.decode())
    #print(data)

    # Remove erased blocks 
    id_set = {block["id"] for block in data["blocks"]}
    for block in Block.objects.all():
        if block.id not in id_set:
            block.delete()
    
    #Parsing du résultat et création des blocs
    position = 0
    for block in data["blocks"]:
        try:
            obj=Block.objects.get(id=block["id"])
            #Pour update un bloc ayant changé de type, de data ou de position
            if obj.type != block["type"] or obj.data !=block["data"] or obj.pos != position:
                obj.type, obj.data, obj.pos = block["type"], block["data"], position
                obj.save()
            created=False
            position += 1
        except:
            obj=Block(type=block["type"], data=block["data"], id=block["id"], pos=position, owner=request.user)
            obj.save()
            created=True
            position += 1
        print(obj, created)
    
    #Création du l'objet JSON à renvoyé à EditorJS
    data={"time":data["time"], "version":data["version"], "blocks":[]}
    for block in Block.objects.order_by("pos"):
        data["blocks"].append({"type":block.type, "data":block.data, "id":block.id})
    
    #Renvoi de la réponse
    return HttpResponse(json.dumps(data))