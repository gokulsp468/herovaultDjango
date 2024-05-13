from rest_framework import serializers
from .models import Discount, DiscountImage

class DiscountImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountImage
        fields = ('id', 'image')

class DiscountSerializer(serializers.ModelSerializer):
    images = DiscountImageSerializer(many=True, read_only=True)

    class Meta:
        model = Discount
        fields = ('id', 'name', 'description', 'isDeleted', 'createdAt', 'updatedAt', 'categoryId', 'storeId', 'images')
        read_only_fields = ['id', 'createdAt', 'updatedAt', 'isDeleted']
