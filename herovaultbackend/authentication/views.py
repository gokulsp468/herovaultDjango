from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from herovaultbackend.decorators import validate_required_fields
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer,CustomTokenObtainPairSerializer
from drf_yasg import openapi
import os
from .tasks import send_otp_email
from rest_framework.settings import api_settings
# Create your views here.

@swagger_auto_schema(method='post', request_body=CustomUserSerializer)
@api_view(['POST'])
@validate_required_fields(['first_name', 'last_name', 'email','mobile_number', 'password'])
def SignUpView(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()            
            user.set_otp()            
            # user.is_active=False       
            user.save()
            # print(user.otp, user.email)
            # send_otp_email(user.email,user.otp)
            response_data = {
                'data':serializer.data,
                'message': 'SignUp successfully'
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        return Response({'error_message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)








class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *kwargs):
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # Access the user object
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                
            })
        else:
            print("fgnfghfg",serializer.errors)
            return Response({'error_message':serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)