from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import login
from django.utils import timezone
from django.core.paginator import Paginator


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
        now = timezone.now()
        posts = user.posts.filter(
            is_published=True,
            pub_date__lte=now) | user.posts.filter(
                is_published=False, pub_date__gte=now)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'profile.html',
                      {'user': user, 'posts': posts, 'page_obj': page_obj})


def custom_404(request, exception):
    return render(request, 'pages/404.html', status=404)


def custom_403(request, exception):
    return render(request, 'pages/403csrf.html', status=403)


def custom_500(request):
    return render(request, 'pages/500.html', status=500)
