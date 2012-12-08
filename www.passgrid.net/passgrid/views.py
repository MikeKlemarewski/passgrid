from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import int_to_base36, base36_to_int
from django.contrib.auth import login as django_login, get_backends
from django.contrib.auth.decorators import login_required

from .forms import UserForm, LoginForm
from .models import Token
from .utils import generate_token, send_verification_email, \
                    verify_passgrid


###
# Views
###

def login(request, template_name="login.html"):
    '''
    An example login page using Passgrid.

    '''
    form = LoginForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        email = form.cleaned_data["email"]
        # email = "john@mobify.com"
        user = User.objects.get(email=email)
        passgrid = request.FILES['passgrid']
        verified = verify_passgrid(user, passgrid)

        if verified:
            backend = get_backends()[0]
            user.backend = '%s.%s' % (backend.__module__, backend.__class__.__name__)
            django_login(request, user)
            return HttpResponseRedirect("/protected/")


        errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                                         forms.util.ErrorList())
        errors.append(unicode("YOU MESSED UP."))


    context = {
        "form": form
    }

    return render(request, template_name, context)

@login_required
def protected(request):
    '''
    An example protected resource page.

    '''
    return render(request, "protected.html")


def home(request):
    return login(request, template_name="home.html")



def signup(request, template_name="home.html"):
    '''
    Allow the user to send an email verification link.

    '''
    form = UserForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data["email"]

        defaults = {
            "username": email,
            "email": email
        }

        user, created = User.objects.get_or_create(email=email,
                                                   defaults=defaults)

        try:
            send_verification_email(user)
        except Exception, err:
            errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                                             forms.util.ErrorList())
            errors.append(unicode(err))
        else:
            messages.success(request, "Email on the way!")
            return HttpResponseRedirect(".")

    context = {
        "form": form
    }
    return render(request, template_name, context)

def verify(request, uidb36, verification_token):
    '''
    Verify an email verification link.

    '''
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(pk=uid_int)
    except (ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user,
                                                        verification_token):
        token, created = generate_token(user)
        context = {
            "token": token.token
        }
        return render(request, "win.html", context)

    return render(request, "fail.html")