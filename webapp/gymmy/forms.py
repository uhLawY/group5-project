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
  
class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        label="Email"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        label="Confirm Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")
        email = cleaned_data.get("email")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email does not exist!")

        return cleaned_data