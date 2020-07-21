from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Listing,Categorie,User,Bid,Comment,Watchlist

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Categorie)
admin.site.register(Bid)

admin.site.register(Watchlist)

admin.site.register(Comment)