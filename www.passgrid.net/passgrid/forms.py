from django import forms


class UserForm(forms.Form):
    email = forms.EmailField(initial="john@mobify.com")


class LoginForm(forms.Form):
    '''
    Passgrid login form.

    '''
    email = forms.EmailField(initial="john@mobify.com")
    passgrid = forms.FileField()