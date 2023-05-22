from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Nom d'utilisateur",
                'class': 'basic_placeholder_inside up'
            }
        ),
        label="",
    )
    password = forms.CharField(
        max_length=63,
        required=True,
        widget=forms.widgets.PasswordInput(
            attrs={
                "placeholder": "Mot de passe",
                'class': 'basic_placeholder_inside'
            }
        ),
        label="",
    )


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)

class AddFollowedForm(forms.Form):
    """
    The unbounded form to register a followed member.
    """
    add_followed = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    followed_name = forms.CharField(
        max_length=150,
        label="Identifiant du membre à suivre",
    )