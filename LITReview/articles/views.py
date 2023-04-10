from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Ticket
from . import forms
from . import models


def index(request):
    latest_ticket_list = Ticket.objects.order_by('-date_created')[:10]
    latest_review_list = Review.objects.order_by('-date_created')[:10]
    context = {
        'latest_ticket_list': latest_ticket_list, 
        'latest_review_list': latest_review_list,
        }
    return render(request, 'articles/index.html', context)


def detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'articles/detail_ticket.html', {'ticket': ticket})

@login_required
def ticket_upload(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if (ticket_form.is_valid()):
            ticket = ticket_form.save(commit=False)
            ticket.creator = request.user
            ticket.save()
            return redirect('/')
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'articles/create_ticket.html', context=context)

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('/')
    context = {
        'ticket': ticket,
        'edit_ticket': edit_form,
    }
    return render(request, 'articles/edit_ticket.html', context=context)

@login_required
def review_and_ticket_upload(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        print(ticket_form.is_valid())
        print(review_form.is_valid())
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('/')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'articles/create_review_and_ticket.html', context=context)