from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



        

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    username = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email','mobile_number', 'password', 'username']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.get('email')
        validated_data['username'] = username
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data={}
        
        username = attrs.get(self.username_field)
        password = attrs.get('password')
        print(username)
        
        
        user = CustomUser.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError("User does not exist.")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")
        
        data['user'] = user
        
        
        return data