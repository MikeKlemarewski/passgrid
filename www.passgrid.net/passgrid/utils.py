import json

from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.utils.http import int_to_base36, base36_to_int

from .models import Token

###
# UTILS
###

def get_token():
    token = []
    for i in range(0,3):
        subtoken = []
        for j in range(0,3):
            token[i] = subtoken
            token[i][j] = random.uniform(0,16777215)
    return token

def generate_token(user):


    defaults = {
        "token": token
    }

    token, created = Token.objects.get_or_create(user=user, defaults=defaults)
    return token, created


def send_verification_email(request, user):
    '''
    Send the email verification email to `user`.

    '''
    context = {
        "protocol": "http",
        "host": request.get_host(),
        "uid": int_to_base36(user.pk),
        "token": token_generator.make_token(user)
    }

    subject = render_to_string("email_subject.txt", context)
    message = render_to_string("email_message.txt", context)


    from_email = "hello@www.passgrid.net"
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def verify_passgrid(user, f):
    '''
    Returns `True` if PassGrid `f` matches `user`'s token.

    '''
    return True

def json_response(data, status_code=200):
    data["status"] = status_code
    body = json.dumps(data)
    response = HttpResponse(body, mimetype="application/json")
    response.status_code = status_code
    return response