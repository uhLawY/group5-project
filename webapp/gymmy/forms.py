from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
from PIL import Image
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)
        if profile.image:
            img = Image.open(profile.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(profile.image.path)
        return profile
  
