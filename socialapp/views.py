from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Follow, Profile


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'socialapp/register.html',
                {'error': 'Username already exists'}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'socialapp/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'socialapp/login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'socialapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    posts = Post.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'socialapp/home.html',
        {'posts': posts}
    )


def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        content = request.POST['content']

        Post.objects.create(
            user=request.user,
            content=content
        )

        return redirect('home')

    return render(request, 'socialapp/create_post.html')


def add_comment(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        text = request.POST['text']

        Comment.objects.create(
            post_id=post_id,
            user=request.user,
            text=text
        )

    return redirect('home')


def like_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = Post.objects.get(id=post_id)

    like = Like.objects.filter(
        post=post,
        user=request.user
    ).first()

    if like:
        like.delete()
    else:
        Like.objects.create(
            post=post,
            user=request.user
        )

    return redirect('home')


def follow_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user_to_follow = User.objects.get(id=user_id)

    if request.user != user_to_follow:
        follow = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow
        ).first()

        if follow:
            follow.delete()
        else:
            Follow.objects.create(
                follower=request.user,
                following=user_to_follow
            )

    return redirect('home')


def profile(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=user_id)

    profile, created = Profile.objects.get_or_create(
        user=user
    )

    posts = Post.objects.filter(
        user=user
    ).order_by('-created_at')

    followers_count = Follow.objects.filter(
        following=user
    ).count()

    following_count = Follow.objects.filter(
        follower=user
    ).count()

    return render(
        request,
        'socialapp/profile.html',
        {
            'profile_user': user,
            'profile': profile,
            'posts': posts,
            'followers_count': followers_count,
            'following_count': following_count,
        }
    )


def followers_list(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=user_id)

    followers = Follow.objects.filter(
        following=user
    )

    return render(
        request,
        'socialapp/followers.html',
        {
            'profile_user': user,
            'followers': followers,
        }
    )


def following_list(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=user_id)

    following = Follow.objects.filter(
        follower=user
    )

    return render(
        request,
        'socialapp/following.html',
        {
            'profile_user': user,
            'following': following,
        }
    )


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        profile.bio = request.POST['bio']

        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']

        profile.save()

        return redirect(
            'profile',
            user_id=request.user.id
        )

    return render(
        request,
        'socialapp/edit_profile.html',
        {'profile': profile}
    )


def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = Post.objects.get(id=post_id)

    if request.user == post.user:
        post.delete()

    return redirect('home')