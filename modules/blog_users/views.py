import json
from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView, UpdateView
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'blog_users/registration/register.html'
    success_url = reverse_lazy('posts-list')


class UserLoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = 'blog_users/registration/login.html'
    success_url = reverse_lazy('posts-list')

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        context = {}
        context['valid'] = True
        return JsonResponse(context)


    def form_invalid(self, form):
        context = {}
        context['valid'] = False
        context['errors'] = form.errors.as_json()
        return JsonResponse(context)

