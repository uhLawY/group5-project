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
    instructions = models.TextField(blank=True, null=True)  
    benefits = models.TextField(blank=True, null=True)  
    popularity_count = models.PositiveIntegerField(default=0) # This area stores count of how often the routine has been added to a workout (popularity).

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



# Models for Flexcam page
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


class FlexcamPost(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/flexcam/')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='flexcam_likes', blank=True)
    
    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

    def liked_by(self):
        return self.likes.all()

    class Meta:
        ordering = ['-date_posted']  # Orders posts with the latest first

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the original save method to save the post

        # Resize the image if necessary
        img = Image.open(self.image.path)
        output_size = (800, 450)  # Set your desired output size here

        # If the image is portrait, resize it to landscape
        if img.height > img.width:
            img = img.resize(output_size, Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        else:
            img.thumbnail(output_size, Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS

        img.save(self.image.path)  # Save the resized image back to the same path



class Comment(models.Model):
    post = models.ForeignKey(FlexcamPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
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

    def save(self, *args, **kwargs):
        if not self.pk: # check if its new
            self.routine.popularity_count += 1  
            self.routine.save() # save in database
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.routine.routine} - {self.reps} reps, {self.sets} sets'



class WorkoutProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_progress')
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE, related_name='progress')
    exercise = models.ForeignKey('WorkoutExercise', on_delete=models.CASCADE, related_name='exercise_progress', null=True, blank=True)
    date = models.DateField(default=timezone.now)
    total_reps = models.PositiveIntegerField(default=0)
    total_sets = models.PositiveIntegerField(default=0)
    total_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    single_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    single_reps = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.workout.name} on {self.date}'


class Report(models.Model):
    post = models.ForeignKey(FlexcamPost, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)