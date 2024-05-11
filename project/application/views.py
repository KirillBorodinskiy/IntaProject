from django.shortcuts import render

# Create your views here.

def index(request):
    r = range(11)
    n = [0,1,2,3,4,5,6,7,8,9,10]
    l = ['Z','A','B','C','D','E','F','G','H','I','J']
    rn = list(zip(r, n))
    rl = list(zip(r, l))
    context = {
        'rn': rn,
        'rl': rl,
        'zi': list(zip(r,n,l)),
        'range':r,
    }
    return render(request, 'application/index.html',context)