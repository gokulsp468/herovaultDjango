from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
# Create your models here.
class CustomUser(AbstractUser):
    
    
    
    mobile_number = models.CharField(blank=True, null=True, default=None, max_length=20)
    status = models.CharField(max_length=2,default=1,null=True)
    otpBelongsToForgotPassword = models.BooleanField(default=False,null=True)
    image_name = models.ImageField(upload_to='user_img/',null=True)
    forgotPasswordOn = models.DateTimeField(blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    
    def generate_otp(self):
        return random.randint(100000, 999999)

    def set_otp(self):
        otp = self.generate_otp()
        self.otp = otp
        # Set the expiry time for OTP (e.g., 10 minutes from now)
        self.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
        
        
    
        
    def __str__(self):
        return self.username

    
    