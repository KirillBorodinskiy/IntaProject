from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'range':range(10)
    }
    return render(request, 'application/index.html',context)