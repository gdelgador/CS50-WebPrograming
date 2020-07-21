from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings

class User(AbstractUser):
    pass


class Categorie(models.Model):
    categorie_name = models.CharField(max_length=50, default="Without categorie",unique=True)

    def __str__(self):
        return f"{self.id}: {self.categorie_name}"

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description =models.TextField(max_length=1000)

    categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE,related_name="categorie_listing")
    # categorie=models.CharField(max_length=100)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, 
                                blank=True, on_delete=models.CASCADE)

    current_bid= models.DecimalField(decimal_places=2,max_digits=6,default=0)

    base_bid= models.DecimalField(decimal_places=2,max_digits=6,default=0)

    image_url = models.URLField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    state = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} : {self.title} "

class Bid(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, 
                                blank=True, on_delete=models.CASCADE)
    # listing=models.CharField(max_length=50)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="bid_listing", default="")
    bid= models.DecimalField(decimal_places=2,max_digits=6, default=0)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, 
                                blank=True, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="comment_listing", default="")
    
    # listing=models.CharField(max_length=50)
    comment= models.TextField(max_length=2000, default="Default")
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id} : {self.author}, {self.listing} "

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="watchlist_listing", default="")
    author= models.ForeignKey(settings.AUTH_USER_MODEL,null=True, 
                                blank=True, on_delete=models.CASCADE)
    watchlist= models.BooleanField(default=False)