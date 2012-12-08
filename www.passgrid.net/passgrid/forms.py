from django import forms


class UserForm(forms.Form):
    email = forms.EmailField(initial="john@mobify.com")