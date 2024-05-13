from rest_framework import serializers
from .models import Category
# from rest_framework.validators import UniqueTogetherValidator
# from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'isDeleted', 'createdAt', 'updatedAt', 'discounts', 'image']
        read_only_fields = ['id', 'createdAt', 'updatedAt', 'discounts', 'isDeleted']
        
    def validate(self, attrs):
        name = attrs.get('name')

        if self.context['request'].method == 'PATCH':
            
            if name and Category.objects.filter(name=name).exists():
                return attrs
        elif name and Category.objects.filter(name=name).exists():
            raise serializers.ValidationError('Category with this name already exists.')
        
        

        return attrs
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Manipulate the image address here
        if representation['image']:
           
           representation['image'] = 'http://127.0.0.1:8000' + representation['image']
        
        return representation
    

    