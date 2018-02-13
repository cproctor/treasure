from django.shortcuts import render

def homepage(request):
    return render(request, 'treasure/homepage.html', {})
