from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import int_to_base36, base36_to_int

from .forms import UserForm
from .models import Token


###
# Views
###

def home(request, template_name="home.html"):
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

###
# UTILS
###

def generate_token(user):
    token = "[[0,4210752,8421504,12632256],[0,4194304,8388608,12582912],[0,16384,32768,49152],[0,64,128,192]]"

    defaults = {
        "token": token
    }

    token, created = Token.objects.get_or_create(user=user, defaults=defaults)
    return token, created


def send_verification_email(user):
    '''
    Send the email verification email to `user`.

    '''
    context = {
        "uid": int_to_base36(user.pk),
        "token": token_generator.make_token(user)
    }

    subject = render_to_string("email_subject.txt", context)
    message = render_to_string("email_message.txt", context)


    from_email = "hello@www.passgrid.net"
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
