import authentication.forms as aForms
import authentication.models as aModels

import django.contrib.auth as dca
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect


def login_page(request):
    form = aForms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = aForms.LoginForm(request.POST)
        if form.is_valid():
            user = dca.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                dca.login(request, user)
                return redirect('articles:flow')
        message = """Merci de vérifier votre
         nom d'utilisateur et votre mot de passe"""

    context = {
        'form': form,
        'message': message
    }

    return render(request, 'authentication/login.html', context=context)


@login_required
def logout_user(request):
    dca.logout(request)
    return redirect('login_page')


def signup_page(request):
    message = ''
    form = aForms.CustomUserCreationForm()
    if request.method == 'POST':
        form = aForms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if password and password2 and password != password2:
                message = 'Veuillez entrer le même mot de passe !'
            else:
                try:
                    password_validation.validate_password(password)
                    user = form.save(commit=False)
                    user.set_password(password)
                    user.save()
                    # auto-login user
                    dca.login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
                except ValidationError as error:
                    message = error

    context = {
        'form': form,
        'message': message
    }

    return render(request, 'authentication/signup.html', context=context)


@login_required
def follows(request):
    """
    Render the "follows" template.
    Use of the AddFollowedForm to register a followed member.
    Render the list of followed members.
    Render the list of followers.
    """
    add_followed_form = aForms.AddFollowedForm()
    followed = request.user.followed_members.all()
    followers = request.user.following_by.all().order_by('user')
    message = ""

    if request.method == "POST":
        if "add_followed" in request.POST:
            add_followed_form = aForms.AddFollowedForm(request.POST)
            if add_followed_form.is_valid():
                followed_name = add_followed_form.cleaned_data["followed_name"]
                try:
                    followed_user = aModels.User.objects.get(username=followed_name)
                    user = request.user
                    # Check user self-follow
                    if followed_user == user:
                        message = "Vous ne pouvez pas vous suivre vous même"
                    # Si l'utilisateur ajoute quelqu'un déjà présent dans sa liste d'abonnement
                    elif aModels.UserFollows.objects.filter(
                            user=user,
                            followed_user=followed_user).exists():
                        message = "Déjà présent dans votre liste d'abonnement"
                    # Si tout est bon
                    else:
                        user.followed_members.add(followed_user.id)
                        message = f"""{followed_user.username}
                         ajouté à vos suivis !"""
                        add_followed_form = aForms.AddFollowedForm()
                except ObjectDoesNotExist:
                    message = "Pas de membre avec cet identifiant !"
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
    to_remove = get_object_or_404(aModels.User, id=followed_id)
    request.user.followed_members.remove(to_remove)
    return redirect('authentication:follows')
