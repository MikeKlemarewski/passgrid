import random
import json
import hashlib

from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.utils.http import int_to_base36, base36_to_int


# import cv2 as cv

from .models import Token


###
# UTILS
###

def get_token():
    token = [None]*4
    for i in range(0,4):
        subtoken = [None]*4
        for j in range(0,4):
            token[i] = subtoken
            r = int(random.uniform(40,255))
            g = int(random.uniform(40,255))
            b = int(random.uniform(40,255))
            token[i][j] = r*256*256 + g * 256 + b
    return token

def generate_token(user):

    token = get_token()

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

    token = Token.objects.filter(user=user)[0]
    token = token.token

    m = hashlib.md5()
    m.update(str(token))
    token_image = "image/%s.png" % m.hexdigest()

    result = template_match(token_image, f)

    return True

def json_response(data, status_code=200):
    data["status"] = status_code
    body = json.dumps(data)
    response = HttpResponse(body, mimetype="application/json")
    response.status_code = status_code
    return response


def template_match(test_image, expected_image):
    # from imagematch import template_match

    test_image_handle = cv.imread(test_image, 1)
    expected_image_handle = cv.imread(expected_image, 1)

    # Flip template, because pic from webcam will be backwards.
    template = cv.flip(template, 1)

    result = cv.matchTemplate(img, template, cv.TM_CCORR_NORMED)
    result8 = cv.normalize(result, None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)

    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)

    matched = maxVal > 0.73
    return matched
