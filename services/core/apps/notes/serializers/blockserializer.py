from rest_framework import serializers
from notes.models import Block



class BlockSerializer(serializers.HyperlinkedModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Block
        fields = ['id', 'type', 'data', 'pos']