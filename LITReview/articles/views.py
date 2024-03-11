from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from itertools import chain
from operator import attrgetter
from .models import Review, Ticket
from . import forms
from django.core.exceptions import PermissionDenied


@login_required
def flow(request):
    """
    Renvoies tous les tickets et revues de l'utilisateur et de ses abonnés
    """
    followed_user_ticket_list = []
    followed_user_review_list = []
    ticket_with_review = []
    followed_users = request.user.followed_members.all()

    for followed_user in followed_users:
        followed_user_ticket_list = followed_user_ticket_list + list(chain(Ticket.objects.all().filter(creator=followed_user)))
        followed_user_review_list = followed_user_review_list + list(chain(Review.objects.all().filter(user=followed_user)))

    user_ticket_list = Ticket.objects.all().filter(creator=request.user)
    user_review_list = Review.objects.all().filter(user=request.user)

    ticket_all = Ticket.objects.all()
    review_all = Review.objects.all()
    for ticket in ticket_all:
        for review in review_all:
            if review.ticket == ticket:
                ticket_with_review.append(ticket.pk)

    final_list = sorted(chain(followed_user_ticket_list, followed_user_review_list, user_ticket_list, user_review_list), key=attrgetter('date_created'), reverse=True)
    context = {
        'final_list': final_list, 
        'ticket_with_review': ticket_with_review,
        }
    
    return render(request, 'articles/flow.html', context)

@login_required
def posts(request):
    """
    Renvoies tous les tickets et revues de l'utilisateur uniquement
    """
    ticket_list = Ticket.objects.all().filter(creator=request.user)
    review_list = Review.objects.all().filter(user=request.user)
    final_list = sorted(chain(ticket_list, review_list), key=attrgetter('date_created'), reverse=True)
    context = {
        'final_list': final_list, 
        }
    return render(request, 'articles/posts.html', context)

@login_required
def create_review(request, ticket_id):
    """
    Transformation en création de review
    """
    review_form = forms.ReviewForm()
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if (review_form.is_valid()):
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('articles:flow')

    context = {
        'element': ticket,
        'review_form': review_form,
    }

    return render(request, 'articles/create_review.html', context=context)

# ===========================================
#                Ticket Part
# ===========================================

@login_required
def ticket_upload(request):
    """
    Création d'un ticket
    """
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if (ticket_form.is_valid()):
            ticket = ticket_form.save(commit=False)
            ticket.creator = request.user
            ticket.save()
            return redirect('articles:flow')
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'articles/create_ticket.html', context=context)

@login_required
def edit_ticket_view(request, ticket_id):
    """
    Modification d'un ticket
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Vérification des droits de l'utilisateur pour la modification du ticket
    if ticket.creator != request.user:
        raise PermissionDenied

    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('articles:posts')
    context = {
        'ticket': ticket,
        'edit_ticket': edit_form,
    }
    return render(request, 'articles/edit_ticket.html', context=context)

@login_required
def edit_review_view(request, review_id):
    """
    Modification d'une critique
    """
    review = get_object_or_404(Review, id=review_id)

    # Vérification des droits de l'utilisateur pour la modification de la review
    if review.user != request.user:
        raise PermissionDenied

    edit_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('articles:posts')
    context = {
        'review': review,
        'edit_review': edit_form,
    }
    return render(request, 'articles/edit_review.html', context=context)

@login_required
def del_ticket(request, ticket_id):
    """
    Suppression d'un ticket (la revue associée sera supprimée)
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    # Vérification des droits de l'utilisateur pour la suppression du ticket
    if ticket.creator != request.user:
        raise PermissionDenied
    
    ticket.delete()
    return redirect('articles:posts')

# ===========================================
#                Review Part
# ===========================================

@login_required
def review_and_ticket_upload(request):
    """
    Création d'une revue et de son ticket
    """
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.creator = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('articles:flow')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'articles/create_review_and_ticket.html', context=context)

@login_required
def del_review(request, review_id):
    """
    Suppression d'une revue
    """
    review = get_object_or_404(Review, pk=review_id)

    # Vérification des droits de l'utilisateur pour la suppression de la review
    if review.user != request.user:
        raise PermissionDenied

    review.delete()
    return redirect('articles:posts')