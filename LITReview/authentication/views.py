from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from authentication.models import User

from . import forms


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = "Merci de vérifier votre nom d'utilisateur et votre mot de passe"
        return render(request, 'authentication/login.html', context={'form': form, 'message': message})



def logout_user(request):
    logout(request)
    return redirect('login')


def signup_page(request):
    form = forms.CustomUserCreationForm()
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})    


@login_required
def follows(request):
    """
    Render the "follows" template.
    Use of the AddFollowedForm to register a followed member.
    Render the list of followed members.
    Render the list of followers.
    """
    add_followed_form = forms.AddFollowedForm()
    followed = request.user.followed_members.all()
    followers = request.user.following_by.all().order_by('user')
    message = ""

    if request.method == "POST":
        if "add_followed" in request.POST:
            add_followed_form = forms.AddFollowedForm(request.POST)
            if add_followed_form.is_valid():
                followed_name = add_followed_form.cleaned_data["followed_name"]
                try:
                    followed_user = User.objects.get(username=followed_name)
                    user = request.user
                    user.followed_members.add(followed_user.id)
                    message = f"{followed_user.username} ajouté à vos suivis !"
                    add_followed_form = forms.AddFollowedForm()
                    # return redirect("authentication:follows")
                except ObjectDoesNotExist:
                    message = "Pas de membre avec cet identifiant !"
                    # return redirect("authentication:follows")
    context = {
        "add_followed_form": add_followed_form,
        "followed": followed,
        "followers": followers,
        "message": message
    }
    return render(
        request,
        "authentication/follows.html",
        context=context
    )


@login_required
def remove_followed(request, followed_id=None):
    to_remove = get_object_or_404(User, id=followed_id)
    request.user.followed_members.remove(to_remove)
    return redirect('authentication:follows')

