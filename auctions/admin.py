from django.contrib import admin
from .models import User, Listing, Comment, Category

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
