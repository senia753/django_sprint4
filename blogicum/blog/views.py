from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Category, Post, Comment
from .forms import PostForm, CommentForm, ProfileForm


User = get_user_model()


def category_posts(request, category_slug):
    category = get_object_or_404(Category,
                                 slug=category_slug, is_published=True)
    posts = category.posts.filter(
        is_published=True, pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': page_obj
    })


def index(request):
    posts = Post.objects.filter(
        is_published=True, pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {
        'page_obj': page_obj
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=True,
                             pub_date__lte=timezone.now())
    comments = post.comments.filter(is_approved=True).order_by('-created_at')
    comment_form = CommentForm()
    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {
        'form': form
    })


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.filter(is_published=True).order_by('-pub_date')
    return render(request, 'blog/profile.html', {
        'user_profile': user,
        'posts': posts
    })


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('blog:profile', username=user.username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=user.username)
    else:
        form = ProfileForm(instance=user)
    posts = user.posts.filter(is_published=True).order_by('-pub_date')
    return render(request, 'blog/profile.html', {
        'user_profile': user,
        'posts': posts,
        'form': form
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {
        'form': form
    })


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {
        'form': form
    })


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return redirect('blog:post_detail', post_id=post.id)


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
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return redirect('blog:post_detail', post_id=post_id)
