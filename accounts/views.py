from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
# Create your views here.
VALID_EMAIL = "We just emailed you a temporary login link. The link will only work in this browser session."

def login_form(request):
    return render(request, 'login_form.html')

def validation_sent(request):
    messages.success(request, VALID_EMAIL)
    return redirect(reverse("login"))

def passwordless_login(request, token):
    url = reverse('social:complete', args=('email',))
    url += '?verification_code={}'.format(token)
    return redirect(url)
