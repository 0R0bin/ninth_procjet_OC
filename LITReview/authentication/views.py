from django.shortcuts import get_object_or_404, render, redirect
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
    follow_form = forms.UserFollowsForm(instance=request.user)
    if request.method == 'POST':
        follow_form = forms.UserFollowsForm(request.POST)
        if (follow_form.is_valid()):
            follow = follow_form.save(commit=False)
            follow.remove()
    context = {
        'follow_form': follow_form,
    }
    return render(request, 'authentication/follows.html', context=context)


# <table cellspacing="0" width="100%">
#         <tbody>
#             {% for follower in request.user.subscribed.all %}
#             <tr>
#                 <td style="border: 1px solid #333;">{{ follower }}</td>
#             </tr>
#             {% endfor %}
#         </tbody>
#     </table>    