from django.http import HttpResponse
from django.shortcuts import render

from microblogs.forms import SignUpForms

# Create your views here.
def home(request):
    return render(request, "home.html")

def sign_up(request):
    form = SignUpForms()
    return render(request, 'sign_up.html', {"form": form})


