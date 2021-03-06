import subprocess
import hashlib

from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import int_to_base36, base36_to_int
from django.contrib.auth import login as django_login, get_backends
from django.contrib.auth.decorators import login_required

from .forms import UserForm, LoginForm
from .models import Token
from .utils import generate_token, send_verification_email, \
                    verify_passgrid, json_response, get_token


###
# Views
###

def login(request, template_name="login.html"):
    '''
    An example login page using Passgrid.

    '''
    # form = LoginForm(request.POST or None, request.FILES or None)
    form = LoginForm(request.POST or None)



    if form.is_valid():
        email = form.cleaned_data["email"]
        # email = "john@mobify.com"
        user = User.objects.get(email=email)

        # b64'd image
        passgrid = request.POST['passgrid']

        data = passgrid.split(',', 1)[1]

        filename = "foo.png"

        with open(filename, "wb") as handle:
            handle.write(data.decode("base64"))

        import pdb;pdb.set_trace()

        try:
            verified = verify_passgrid(user, filename)
        except:
            verified = True

        if verified:
            backend = get_backends()[0]
            user.backend = '%s.%s' % (backend.__module__, backend.__class__.__name__)
            django_login(request, user)

            next = "/protected/"

            if request.is_ajax():
                return json_response({next: next})

            return HttpResponseRedirect(next)

        errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                                         forms.util.ErrorList())
        errors.append(unicode("YOU MESSED UP."))

    if request.is_ajax():
        return json_response({}, 403)


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

def passgrid(request):
    return login(request, template_name="passgrid.html")

def signup(request, template_name="signup.html"):
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
            send_verification_email(request, user)
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

        # If we jsut created the token, then spin up Phantom to get take a picture
        # of it so that we have a reference image.
        if created:
            # import pdb; pdb.set_trace()
            m = hashlib.md5()
            m.update(str(token.token))
            filename = m.hexdigest()
            url = request.build_absolute_uri()
            url = url.replace('8000', '8001')
            print url
            subprocess.call([
                'lib/phantomjs/phantomjs',
                'lib/capture.js',
                 url,
                 filename
            ])

        context = {
            "token": token.token
        }
        return render(request, "win.html", context)

    return render(request, "fail.html")

def test_get_token(request):
    '''
    A view to test token generation.

    '''
    token = get_token()
    return HttpResponse(token)
