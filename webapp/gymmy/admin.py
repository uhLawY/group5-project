from django.contrib import admin
from .models import Post, Profile, Category, Routines
from .models import Profile, WorkoutProgress
from .models import FlexcamPost, Comment , Report
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Routines)
admin.site.register(WorkoutProgress)


admin.site.register(FlexcamPost)
admin.site.register(Comment)
admin.site.register(Report)