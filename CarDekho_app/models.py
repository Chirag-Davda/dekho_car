from django.db import models


class Carlist(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    chassinumber = models.CharField(max_length=100,blank=True,null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
    
class Showroomlist(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    website = models.URLField(max_length=200)
    
    def __str__(self) -> str:
        return self.name
    