from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Category, Post, Comment
from .forms import PostForm, CommentForm, ProfileForm
from django.http import Http404
from django.db.models import Count, Q


User = get_user_model()


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    posts = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).annotate(
        comment_count=Count('comments', filter=Q(comments__is_approved=True))
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': page_obj,
    })


def index(request):
    posts = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).annotate(
        comment_count=Count('comments', filter=Q(comments__is_approved=True))
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {
        'page_obj': page_obj
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if (
        (not post.is_published or post.pub_date > timezone.now())
        and (not request.user.is_authenticated or request.user != post.author)
    ):
        raise Http404("Post is not available")
    comments = post.comments.filter(is_approved=True).order_by('-created_at')
    form = CommentForm()
    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:profile', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html',
                  {'form': form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).annotate(
        comment_count=Count('comments', filter=Q(comments__is_approved=True))
    ).order_by('-pub_date')
    if not request.user.is_authenticated or request.user != user:
        posts = posts.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/profile.html', {
        'profile': user,
        'posts': posts,
        'page_obj': page_obj,
    })


@login_required
def edit_profile(request, username=None):
    if username is None:
        user = request.user
    else:
        user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('blog:profile', username=user.username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.save()
            return redirect('blog:profile', username=user.username)
    else:
        form = ProfileForm(instance=user)
    posts = user.posts.filter(is_published=True).order_by('-pub_date')
    return render(request, 'blog/user.html', {
        'user': request.user,
        'posts': posts,
        'form': form
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm(user=request.user)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post,
                        user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post, user=request.user)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return redirect('blog:detail', post_id=post.id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id=post.id)
    return redirect('blog:post_detail', post_id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment.html', {
        'form': form,
        'comment': comment
    })


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    comment.delete()
    return redirect('blog:post_detail', post_id=post_id)
