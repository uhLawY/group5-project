from django.contrib import admin
from .models import Post, Profile, Category, Routines
from .models import Profile

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Routines)
