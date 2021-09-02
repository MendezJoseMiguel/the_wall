from django.shortcuts import render, HttpResponse, redirect
#decorador para autentificar el login

def login_required(func):
    
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session:
            return redirect('/login')
        resp = func(request, *args, **kwargs)
        return resp
    
    return wrapper