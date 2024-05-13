from django.db import models
import uuid
from category.models import Category
from store.models import Store

import uuid
from django.db import models

class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    isDeleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    categoryId = models.ForeignKey(Category, verbose_name=("category"), on_delete=models.CASCADE)
    storeId = models.ForeignKey(Store, verbose_name=("store"), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class DiscountImage(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='discount_images/',null=True,blank=True)

    def __str__(self):
        return f"Image for {self.discount.name}"

