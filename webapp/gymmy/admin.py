from django.contrib import admin
from .models import Post, Profile, Category, Routines
from .models import Profile, WorkoutProgress

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Routines)
admin.site.register(WorkoutProgress)
from .models import FlexcamPost, Comment

admin.site.register(FlexcamPost)
admin.site.register(Comment)