from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Users,Post, Comments
from django.http import HttpResponseRedirect
import bcrypt
from .decorators import login_required
from django.db import IntegrityError


@login_required
def index(request):
    
    return redirect('/wall')


@login_required
def wall(request):
    users = Users.objects.all()
    posts = Post.objects.all()
    comments = Comments.objects.all()

    context = {
        'users' : users,
        'posts' : posts,
        'comments' : comments

    }

    return render(request,'index.html', context)

def login(request):
    #si llega un get, renderizamos la pagina del registro
    if request.method =='GET':
        return render(request,'login.html')
    else:
        email = request.POST['email']
        password = request.POST['password']

    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        messages.error(request,'Usuario inexistente o contraseña incorrecta')
        return redirect('/login')

    #si llegamos aca, estamos seguro que el usuario existe 
    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        messages.error(request,'Usuario inexistente o contraseña incorrecta')
        return redirect('/login')

    #si llegamos hasta aca, estamos seguros que el usuario existe y la contraseña es correcta
    request.session['user'] = {
        'id' : user.id,
        'first_name' : user.first_name,
        'last_name' : user.first_name,
        'email' : user.email,
        'avatar' : user.avatar
    }
    messages.success(request, f'Hola {user.first_name} {user.last_name}')
    return redirect('/wall')

@login_required
def logout(request):
    del request.session['user']
    return redirect('/register')

def register(request):
    #si llega un get, renderizamos la pagina del registro
    if request.method =='GET':
        return render(request,'register.html')
    else:
        #si llega un POST tomamos los valores del formulario
        #y creamos un nuevo usuario
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        #validar que el formulario este correcto

        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            #se es mayor a cero, hay al menos un error
            #entonces le mostramos los errores al usuario
            for llave,mensaje_de_error in errors.items():
                messages.error(request,mensaje_de_error)

            return redirect('/register')

    users = Users.objects.create(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    )

    request.session['user'] = {
        'id' : users.id,
        'first_name' : users.first_name,
        'last_name' : users.last_name,
        'email' : users.email,
        'avatar' : users.avatar,
    }
    messages.success(request,'Usuario creado con exito')
    return redirect('/wall')

def create_messages(request):
    post = request.POST['post']
    user_id = request.session['user']['id']

    print(user_id)
    posts = Post.objects.create(
        post = post,
        user_id = user_id
    )

    request.session['post'] = {
        'id':posts.id,
        'post':posts.post,
        'user_poster_first': request.session['user']['first_name'],
        'user_poster_last': request.session['user']['last_name'],
        'user_poster_id' : user_id
    }

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))