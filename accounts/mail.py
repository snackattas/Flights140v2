import os
import requests
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from social_django.middleware import SocialAuthBaseException

# Send mail validation to user, the email should include a link to continue the
# auth process. This is a simple example, it could easilly be extended to
# render a template and send a fancy HTML email instad.
INVALID_EMAIL_ERROR = "{email} is an invalid email. Please enter a valid email."
MESSAGE = "Use this link to login:\n{url} \n\n**Note that this link only works one time.\n It must be clicked within the same browser session that accessed flights140.com"


def send_validation(strategy, backend, code):
    email = code.email
    mailgun_validate(email)
    url = reverse('passwordless_login', args=(code.code,))
    url = strategy.request.build_absolute_uri(url)
    try:
        send_mail(
            subject='Passwordless Login from Flights140',
            message=MESSAGE.format(url=url),
            from_email=os.environ.get("HOST_EMAIL"),
            recipient_list=[email],
            fail_silently=False)
    except:
        raise SocialAuthBaseException(\
            INVALID_EMAIL_ERROR.format(email=email))

def mailgun_validate(email):
    """Uses mailgun api to verify if an email is valid syntax and also does some degree of validating.  It is not perfect though"""
    try:
        request = requests.get(
            url="https://api.mailgun.net/v3/address/validate",
            auth=("api", os.environ.get('MAILGUN_API_KEY')),
            params={"address": email})
    except:
        raise SocialAuthBaseException("Internal error. Reload the page and try again or contact a site administrator.")
    if not request.json().get("is_valid"):
        raise SocialAuthBaseException(\
            INVALID_EMAIL_ERROR.format(email=email))
