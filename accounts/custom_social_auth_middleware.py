from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from social_core.exceptions import AuthMissingParameter
from social_django.middleware import SocialAuthExceptionMiddleware


class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if type(exception) == AuthMissingParameter:
            messages.error(request, "Your link has expired.  Please proceed through the email login process again.")
        else:
            pass
