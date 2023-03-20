from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import login, authenticate, logout # import des fonctions login et authenticate
from django.views.generic import View
from django.conf import settings

from . import forms

class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = forms

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})



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

def user_follows(request):
    return render(request, 'authentication/follows.html')