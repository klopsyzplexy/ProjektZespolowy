from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')


def singup(requset):
    if requset.method == 'POST':
        username = requset.POST['username']
        email = requset.POST['email']
        password = requset.POST['password']
        password2 = requset.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(requset, 'Istnieje użytkownik przypisany do adresu e-mail')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(requset, 'Nazwa użytkownika jest zajęta')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #logowanie użytkownika i przekierowanie do ustawień

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, u_id=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(requset, 'Hasła różnią się od siebie')
            return redirect('signup')
    else:
        return render(requset, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Niepoprawne dane')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
