from django.shortcuts import render

def homepage(request):
    return render(request, 'treasure/homepage.html', {})

def crossdomain(request):
    return render(request, 'treasure/crossdomain.xml', {}, content_type="text/xml")

def extension(request):
    return render(request, 'treasure/extension.js', {}, content_type="application/javascript")
