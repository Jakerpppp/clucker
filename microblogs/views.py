from typing import Any
from django import http
from django.http import HttpResponse
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
    

class LogInView(View):
    '''Log In View'''

    http_method_names = ['get', 'post']

    @method_decorator(login_prohibited)
    def dispatch(self, request):
        return super().dispatch(request)


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

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required
def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(author = user)
        following = request.user.is_following(user)
        followable = request.user != user
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        return render(request, 'show_user.html', {'user': user, "posts" : posts, "following": following, "followable": followable})
    
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


