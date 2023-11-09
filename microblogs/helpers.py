from django.shortcuts import redirect, render
from django.conf import settings



def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            #if the user is authenicated, they go to the feed screen
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            #otherwise we call the view_function withe the request
            return view_function(request)
    return modified_view_function