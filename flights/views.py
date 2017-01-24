from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

from functools import wraps

# Create your views here.
def requires_login(function):
    """This is a decorator that checks the request.user that is passed in by python social auth processes to confirm that python social auth worked.  If python social auth processes are not cleared, the decorator redirects to the login page."""

    @wraps(function)
    def decorated_function(*args, **kwargs):
        request = args[0]
        if not request.user or request.user.is_anonymous:
            return redirect('/')
        else:
            return function(*args, **kwargs)
    return decorated_function

def login(request):
    return render(request, 'login.html')

@requires_login
def loggedin(request):
    return render(request, 'loggedin.html')

def logout(request):
    auth_logout(request)
    return redirect('/')
