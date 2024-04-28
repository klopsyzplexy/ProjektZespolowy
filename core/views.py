from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile, Post
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    posts = Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts})


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
                user_login = auth.authenticate(username=username, password=password)
                auth.login(requset, user_login)
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, u_id=user_model.id)
                new_profile.save()
                return redirect('settings')
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


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            user_profile.profile_img = user_profile.profile_img
            user_profile.bio = request.POST['bio']
            user_profile.fav_couisine = request.POST['fav_couisine']

            user_profile.save()
        else:
            user_profile.profile_img = request.FILES.get('image')
            user_profile.bio = request.POST['bio']
            user_profile.fav_couisine = request.POST['fav_couisine']

            user_profile.save()
        return redirect('settings')
    return render(request, 'settings.html', {'user_profile': user_profile})


def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image = image, caption = caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
    }
    return render(request, 'profile.html', context)

