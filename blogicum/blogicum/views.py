from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import login


class UserRegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/registration.html',
                      {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', username=user.username)
        return render(request, 'registration/registration.html',
                      {'form': form})


class UserProfileView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        posts = user.posts.all()
        return render(request, 'profile.html',
                      {'user': user, 'posts': posts})


def custom_404(request, exception):
    return render(request, 'pages/404.html', status=404)


def custom_403(request, exception):
    return render(request, 'pages/403csrf.html', status=403)


def custom_500(request):
    return render(request, 'pages/500.html', status=500)
