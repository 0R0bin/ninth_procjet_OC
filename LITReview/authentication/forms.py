from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
# from authentication.models import UserFollows

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")

class AddFollowedForm(forms.Form):
    """
    The unbounded form to register a followed member.
    """
    add_followed = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    followed_name = forms.CharField(
        max_length=150,
        label="Identifiant du membre à suivre",
    )