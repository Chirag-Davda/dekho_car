from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

class Carlist(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    chassinumber = models.CharField(max_length=100,blank=True,null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    showroom = models.ForeignKey('Showroomlist', on_delete=models.CASCADE, related_name='showroom',null=True)
    
    def __str__(self) -> str:
        return self.name
    
class Showroomlist(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    website = models.URLField(max_length=200)
    
    def __str__(self) -> str:
        return self.name
    
class Review(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator,MaxValueValidator])
    comment = models.CharField(max_length=200, null=True)
    car = models.ForeignKey(Carlist, on_delete=models.CASCADE, related_name='Review')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "The Rating Is" + self.car.name + " :--- " + str(self.rating)