from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone



# Create your models here.
class books(models.Model):
    title=models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description=models.TextField(blank=True)
    published_date = models.DateTimeField(default=timezone.now) 
    price=models.DecimalField(max_digits=30, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if not self.title:
            raise ValidationError('Title must not be empty.') 
        def __str__(self):
            return self.title
        


        
