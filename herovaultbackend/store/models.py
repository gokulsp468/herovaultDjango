from django.db import models
import uuid
# Create your models here.
class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    image_name = models.ImageField(upload_to='store_img/',null=True,blank=True)
    website = models.URLField(null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name