from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not username or not email or not password1 or not password2:
            raise forms.ValidationError("All fields are required.")

        if password1 != password2:
            raise forms.ValidationError("The passwords do not match.")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")

        return cleaned_data