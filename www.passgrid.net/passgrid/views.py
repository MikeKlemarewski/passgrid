from django.shortcuts import render


def home(request, template_name="home.html"):
    context = {}
    return render(request, template_name, context)


def mobile(request, template_name="mobile.html"):
    context = {}
    return render(request, template_name, context)

