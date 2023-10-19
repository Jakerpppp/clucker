from django.http import HttpResponse
from django.shortcuts import redirect, render

from microblogs.forms import LogInForm, SignUpForms

# Create your views here.
def home(request):
    return render(request, "home.html")

def feed(request):
    return render(request, "feed.html")

def log_in(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
    else:
        form = LogInForm()
    return render(request, "log_in.html", {"form": form})

def sign_up(request):
    if request.method == "POST":
        form = SignUpForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect("feed")
    else:
        form = SignUpForms()
    return render(request, 'sign_up.html', {"form": form})


