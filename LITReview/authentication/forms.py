from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from authentication.models import UserFollows

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")

class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ('followed_user',)

# class AddFollow(forms.ModelForm):
#     delete_user = forms.BooleanField(widget=forms.HiddenInput, initial=False)

class DelFollow(forms.ModelForm):
    delete_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)