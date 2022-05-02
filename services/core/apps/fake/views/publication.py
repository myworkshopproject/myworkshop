from django.views.generic.list import ListView

from fake.models import Publication


class PublicationView(ListView):
    model = Publication
