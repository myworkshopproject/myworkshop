from attr import fields

from rest_framework import serializers
from notes.models import Block



class BlockSerializer(serializers.HyperlinkedModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Block
        fields = ['id', 'type', 'data']
        #fields = ['url', 'id', 'created', 'type', 'data', 'owner']