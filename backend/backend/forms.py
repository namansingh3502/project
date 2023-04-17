from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = UserProfile
        fields = (
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
            'phone',
        )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = UserProfile.objects.exclude(pk=self.instance.pk).get(email=email)
        except UserProfile.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account.email)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = UserProfile.objects.exclude(pk=self.instance.pk).get(username=username)
        except UserProfile.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)
