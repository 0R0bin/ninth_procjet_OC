from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket
from . import forms
from . import models


def index(request):
    latest_ticket_list = Ticket.objects.order_by('-date_created')[:5]
    context = {'latest_ticket_list': latest_ticket_list}
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