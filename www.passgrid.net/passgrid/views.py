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

def verify(request, uidb36, token, template_name="verify.html"):
    '''
    Verify an email verification link.

    '''
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(pk=uid_int)
    except (ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        verified = True
    else:
        verified = False

    context = {
        "verified": verified
    }

    return render(request, template_name, context)


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
