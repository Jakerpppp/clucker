from typing import Any
from django import http
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from microblogs.forms import LogInForm, SignUpForms, PostForm, UserForm, PasswordForm
from .models import Post, User
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .helpers import login_prohibited
from django.contrib.auth.hashers import check_password
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

@login_prohibited
def home(request):
    return render(request, "home.html")


class FeedView(LoginRequiredMixin, ListView):
    """Class-based generic view for displaying a view."""

    model = Post
    template_name = "feed.html"
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the user's feed."""
        current_user = self.request.user
        authors = list(current_user.followees.all()) + [current_user]
        posts = Post.objects.filter(author__in=authors)
        return posts

    def get_context_data(self, **kwargs):
        """Return context data, including new post form."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = PostForm()
        return context

def log_out(request):
    logout(request)
    return redirect("home")

@login_required
def follow_toggle(request, user_id):
    current_user = request.user
    try:
        followee = User.objects.get(id = user_id)
        current_user.toggle_follow(followee)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        return redirect('show_user', user_id)
        


class LogInProhibitedMixin:
    redirect_when_logged_in = None

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        else:
            return super().dispatch(*args, **kwargs)
        
    def get_redirect_when_logged_in(self):
        if self.redirect_when_logged_in is None:
            raise ImproperlyConfigured
        else:
            return self.redirect_when_logged_in
        
    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in()
        return redirect(url)


    

class LogInView(LogInProhibitedMixin,View):
    '''Log In View'''

    http_method_names = ['get', 'post']
    redirect_when_logged_in = 'feed'


    def get(self, request):
        '''Display Log In View'''
        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        '''Handle Log In Attempt'''
        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or 'feed'
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The Credentials Provided were Invalid")
        return self.render()

    def render(self):
        form = LogInForm()
        return render(self.request, "log_in.html", {"form": form, "next" : self.next})


class SignUpView(LogInProhibitedMixin, FormView):
    """View that signs up user."""

    form_class = SignUpForms
    template_name = "sign_up.html"
    redirect_when_logged_in = "feed"

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("feed")

class NewPostView(LoginRequiredMixin, CreateView):
    """Class-based generic view for new post handling."""

    model = Post
    template_name = 'feed.html'
    form_class = PostForm
    http_method_names = ['post']

    def form_valid(self, form):
        """Process a valid form."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Return URL to redirect the user too after valid form handling."""
        return reverse('feed')

    def handle_no_permission(self):
        return redirect('log_in')

class UserListView(LoginRequiredMixin, ListView):
    '''Creates a List of all Users'''
    model = User
    template_name = 'user_list.html'
    context_object_name = "users" #Stores the list of all users in the 'users' variable


class ShowUserView(LoginRequiredMixin, DetailView):
    '''Shows individual Data'''
    model = User
    template_name = 'show_user.html'
    context_object_name = "user"
    pk_url_kwarg = 'user_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(author = user)
        context['following'] = self.request.user.is_following(user)
        context['followable'] = self.request.user != user
        return context
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect('user_list')

    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View to update logged-in user's profile."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse("feed")

@login_required
def password(request):
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.add_message(request, messages.SUCCESS, "Password updated!")
                return redirect('feed')
    form = PasswordForm()
    return render(request, 'password.html', {'form': form})


