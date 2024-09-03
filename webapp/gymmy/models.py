from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Get the old image file path before saving the new one
        old_profile = Profile.objects.get(id=self.id) if self.id else None
        old_image_path = old_profile.image.path if old_profile else None

        super().save(*args, **kwargs)

        # Delete the old image from the media folder if a new image is uploaded
        if old_image_path and os.path.exists(old_image_path) and old_profile.image != self.image:
            if old_profile.image.name != 'default.jpg':  # Ensure the default image is not deleted
                os.remove(old_image_path)

        # Resize the new profile picture if necessary
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
# Models for Routine page

class Category(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

class Routines(models.Model):
    routine = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/routine/')
    favorites = models.ManyToManyField(User, related_name='favourite_routines', blank=True)

    def __str__(self):
        return self.routine
    
    class Meta:
        verbose_name_plural = 'routines'


class Post(models.Model):
    title= models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    routine = models.ForeignKey(Routines, on_delete=models.CASCADE)
    reps = models.PositiveIntegerField(default=1)  
    sets = models.PositiveIntegerField(default=1)  

    def __str__(self):
        return f'{self.routine.routine} - {self.reps} reps, {self.sets} sets'




