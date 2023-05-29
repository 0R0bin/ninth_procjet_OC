from django import forms

from . import models


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    title = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "",
                'class': 'basic_placeholder_outside'
                
            }
        ),
        label="Titre",
    )

    description = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "",
                'class': 'basic_placeholder_outside'
            }
        ),
        label="Description",
    )

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': '',
        }

class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre',
            'rating': 'Note',
            'body': 'Commentaire',
        }