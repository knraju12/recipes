from django.shortcuts import render,redirect
from .models import Recipes
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

def home(request):
    return render(request,'raj/option.html')


def register(request):
    return render(request,'raj/registration.html')

def login_data(request):
    if request.method == "POST" :
        user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password'],
                                        email=request.POST['email'],
                                        first_name = request.POST['first_name'],
                                        last_name = request.POST['last_name'])
        user.set_password('password')
        #user.save()
    return render(request,'raj/login.html')


def check(request):
    #import pdb; pdb.set_trace()
    user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
    print(user)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/raj/recipe_list/')
    else:
        return HttpResponseRedirect('/raj/register/')

def logout_data(request):
    logout(request)
    return HttpResponseRedirect('/raj/login/')

@login_required(login_url='/raj/login/')
def recipe_list(request):
    recipe = Recipes.objects.all()
    return render(request,'raj/recipe_details.html', {"recipes": recipe})


@login_required(login_url='/raj/login/')
def create(request):
    return render(request,'raj/create.html')

@login_required(login_url='/raj/login/')
def data(request):
    Recipes.objects.create(name = request.POST["name"],
                           ingredients = request.POST["ingredients"],
                           process = request.POST["process"],
                           image = request.FILES["image"])
    return HttpResponseRedirect('/raj/recipe_list/')

@login_required(login_url='/raj/login/')
def details(request,recipe_id):
    recipe = Recipes.objects.get(id = recipe_id)
    return render(request,'raj/details.html',{'recipes':recipe})


@login_required(login_url='/raj/login/')
def delete(request,recipe_id):
    Recipes.objects.get(id = recipe_id).delete()
    return HttpResponseRedirect('/raj/recipe_list/',{recipe_id})


@login_required(login_url='/raj/login/')
def my_view(request):
    if not request.user.is_authenticated:
        return render(request, 'raj/error.html')
    else:
        return HttpResponseRedirect('/raj/recipe_list/')
