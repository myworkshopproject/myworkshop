from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from accounts.models import User


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User

    fields = [
        "image",
        "first_name",
        "last_name",
        "source",
    ]

    template_name = "accounts/profile.html"

    success_message = _("Profile successfully changed.")

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return User.public_objects.all()

    context_object_name = "member"


class UserListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return User.public_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": _("Members"),
            "description": _("The list of registered members."),
        }
        return context
