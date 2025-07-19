from django.shortcuts import resolve_url, render
from django.http import Http404
from django.views import View, generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from .models import UserProfile
from .forms import UserProfileForm


# Create your views here.
class UserProfileUpdateView(generic.UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    context_object_name = 'instance'
    template_name = 'user_profile/form.html'
    success_message = "User Updated Success."
    title = "User Profile Update Form"
    success_url = reverse_lazy("home")


    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.save()

        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
    