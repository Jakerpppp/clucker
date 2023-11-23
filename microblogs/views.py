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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured

@login_prohibited
def home(request):
    return render(request, "home.html")


@login_required
def feed(request):
    form = PostForm()
    current_user = request.user
    authors = list(current_user.followees.all()) + [current_user]
    posts = Post.objects.filter(author__in=authors)
    return render(request, "feed.html", {"form": form, "posts" : posts, 'user': current_user})

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
        url = self.get_redirect_when_logged_in
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


@login_prohibited
def sign_up(request):
    if request.method == "POST":
        form = SignUpForms(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = SignUpForms()
    return render(request, 'sign_up.html', {"form": form})

def new_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            current_user = request.user
            form = PostForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                post = Post.objects.create(author=current_user, text=text)
                return redirect('feed')
            else:
                return render(request, 'feed.html', {'form': form})
        else:
            return redirect('log_in')
    else:
        return HttpResponseForbidden()

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

    
@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('feed')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'profile.html', {'form': form})

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


