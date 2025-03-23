from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import BlogPost, Comment, Category, UserProfile
from .forms import BlogPostForm, CommentForm, UserProfileForm
from django.utils.text import slugify

def home(request):
    """Home page view"""
    latest_posts = BlogPost.objects.all().order_by('-created_at')[:6]  # Get the 6 most recent posts
    return render(request, 'blog/home.html', {
        'latest_posts': latest_posts
    })

def blog_list(request):
    """List all blog posts"""
    posts = BlogPost.objects.all()
    categories = Category.objects.all()
    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'categories': categories
    })

def post_detail(request, slug):
    """Detail view for a blog post"""
    post = get_object_or_404(BlogPost, slug=slug)
    comments = post.comments.all()
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('blog:post_detail', slug=slug)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def post_create(request):
    """Create a new blog post"""
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Generate a unique slug
            base_slug = slugify(post.title)
            unique_slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = unique_slug
            post.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Your post has been created!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})

@login_required
def post_edit(request, slug):
    """Edit an existing blog post"""
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})

@login_required
def post_delete(request, slug):
    """Delete a blog post"""
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('blog:blog_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def blogger_list(request):
    """List all bloggers"""
    bloggers = User.objects.filter(blog_posts__isnull=False).distinct()
    return render(request, 'blog/blogger_list.html', {'bloggers': bloggers})

def blogger_detail(request, username):
    """Detail view for a blogger"""
    blogger = get_object_or_404(User, username=username)
    posts = blogger.blog_posts.all()
    return render(request, 'blog/blogger_detail.html', {
        'blogger': blogger,
        'posts': posts
    })

@login_required
def profile_edit(request):
    """Edit user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('blog:blogger_detail', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'blog/profile_form.html', {'form': form})

def search_posts(request):
    """Search blog posts"""
    query = request.GET.get('q')
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()
    else:
        posts = BlogPost.objects.none()
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

@login_required
def like_post(request, slug):
    """Like a blog post"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
        
    post = get_object_or_404(BlogPost, slug=slug)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
        liked = True
        
    return JsonResponse({
        'liked': liked,
        'likes_count': post.get_likes_count(),
        'dislikes_count': post.get_dislikes_count()
    })

@login_required
def dislike_post(request, slug):
    """Dislike a blog post"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
        
    post = get_object_or_404(BlogPost, slug=slug)
    
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
        disliked = False
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user)
        disliked = True
        
    return JsonResponse({
        'disliked': disliked,
        'likes_count': post.get_likes_count(),
        'dislikes_count': post.get_dislikes_count()
    })

def register(request):
    """Register a new user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'registration/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'registration/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'registration/register.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.create(user=user)
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'registration/register.html')

def logout_view(request):
    """Custom logout view"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('blog:home')

def category_posts(request, slug):
    """View posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(categories=category)
    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'category': category
    })
