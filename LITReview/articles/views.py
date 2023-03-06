from django.shortcuts import render, get_object_or_404
from .models import Ticket


def index(request):
    latest_ticket_list = Ticket.objects.order_by('-date_created')[:5]
    context = {'latest_ticket_list': latest_ticket_list}
    return render(request, 'articles/index.html', context)


def detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'articles/detail_ticket.html', {'ticket': ticket})