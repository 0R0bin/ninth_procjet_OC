from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, password_validation
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Nom d'utilisateur",
                'class': 'basic_placeholder_inside'
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


class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=63,
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Nom d'utilisateur",
                'class': 'basic_placeholder_inside'
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
    password2 = forms.CharField(
        max_length=63,
        required=True,
        widget=forms.widgets.PasswordInput(
            attrs={
                "placeholder": "Confirmer le mot de passe",
                'class': 'basic_placeholder_inside'
            }
        ),
        label="",
    )

    class Meta():
        model = get_user_model()
        fields = ['username', 'password']


class AddFollowedForm(forms.Form):
    """
    The unbounded form to register a followed member.
    """
    followed_name = forms.CharField(
        max_length=150,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Membre à suivre",
                'class': 'basic_placeholder_outside'
            }
        ),
        label="",
    )
    add_followed = forms.BooleanField(widget=forms.HiddenInput, initial=True)
