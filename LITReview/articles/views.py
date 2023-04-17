from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from itertools import chain
from operator import attrgetter
from .models import Review, Ticket
from . import forms
from . import models

@login_required
def flow(request):
    latest_ticket_list = Ticket.objects.order_by('-date_created')[:10]
    latest_review_list = Review.objects.order_by('-date_created')[:10]
    context = {
        'latest_ticket_list': latest_ticket_list, 
        'latest_review_list': latest_review_list,
        }
    return render(request, 'articles/flow.html', context)

@login_required
def posts(request):
    ticket_list = Ticket.objects.all().filter(creator=request.user)
    review_list = Review.objects.all().filter(user=request.user)
    final_list = sorted(chain(ticket_list, review_list),key=attrgetter('date_created'))
    context = {
        'final_list': final_list, 
        }
    return render(request, 'articles/posts.html', context)

@login_required
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
def edit_ticket_view(request, ticket_id):
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
            return redirect('/')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'articles/create_review_and_ticket.html', context=context)