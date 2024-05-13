from rest_framework import serializers
from .models import Store

   

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'description', 'contact_number', 'createdAt', 'updatedAt', 'website', 'image_name','location']
        read_only_fields = ['id', 'createdAt', 'updatedAt']
        
    def validate(self, attrs):
        name = attrs.get('name')

        if self.context['request'].method == 'PATCH':
            
            if name and Store.objects.filter(name=name).exists():
                return attrs
        elif name and Store.objects.filter(name=name).exists():
            raise serializers.ValidationError('store with this name already exists.')
        
        

        return attrs
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Manipulate the image address here
        if representation['image_name']:
           
           representation['image_name'] = 'http://127.0.0.1:8000' + representation['image_name']
        
        return representation
    

    