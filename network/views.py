from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
import json

from .models import *


def index(request):

    if request.method == "POST":
        if request.POST["body"]:
            body = request.POST["body"]
            new_post = Post(user=User.objects.get(pk=request.user.id), body=body)
            new_post.save()
            confirmation = True
            error = False
        else:
            error = True
            confirmation = False
            
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(posts, 10)

        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        return render(request, "network/index.html", {
            "posts": post,
            "confirmation": confirmation,
            "error": error,
        })
    else: 
        try:
            posts = Post.objects.all()
            posts = posts.order_by("-timestamp").all() 
        except Post.DoesNotExist:
            return render(request, "network/index.html",{
                "not_exist": True,
            })
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(posts, 10)
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        return render(request, "network/index.html", {
            "posts": post,
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def user(request, user_id):
    if request.method == "POST":
        user = User.objects.get(pk=int(request.POST["follow"]))
        try:
            follower = Followers.objects.get(user=user, unique = user.pk, follower_id=request.user.id)
            follower.delete()
            follow_button = True
        except Followers.DoesNotExist:
            new_follow = Followers(user=user, unique = user.pk, follower_id=request.user.id)
            new_follow.save()
            follow_button = False

        profile_user  = User.objects.get(pk=user_id)
        if request.user.id == profile_user.id:
            follow = False
        else:
            follow = True
        try:
            followers = Followers.objects.filter(user=profile_user).count()
        except Followers.DoesNotExist:
            followers = 0
        
        try:
            following = Followers.objects.filter(follower_id=user.pk).count()
 
        except Followers.DoesNotExist:
            following = 0
        
        try:
            posts = Post.objects.filter(user=profile_user)
            posts = posts.order_by("-timestamp").all() 

        except Post.DoesNotExist:
            return render(request, "network/index.html",{
                "not_exist": True,
            })
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(posts, 10)

        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        return render(request, "network/profile.html", {
            "user": profile_user,
            "followers": followers,
            "following": following,
            "posts": post,
            "follow": follow,
            "follow_button": follow_button,
        })
    else:
        if not request.user.is_authenticated:
                try:
                    posts = Post.objects.all()
                    posts = posts.order_by("-timestamp").all() 
                except Post.DoesNotExist:
                    return render(request, "network/index.html",{
                        "not_exist": True,
                    })
                # Pagination
                page = request.GET.get('page')
                paginator = Paginator(posts, 10)
                try:
                    post = paginator.page(page)
                except PageNotAnInteger:
                    post = paginator.page(1)
                except EmptyPage:
                    post = paginator.page(paginator.num_pages)

                return render(request, "network/index.html", {
                    "posts": post,
                })

        else:
            profile_user  = User.objects.get(pk=user_id)
            if request.user.id == profile_user.id:
                follow = False
            else:
                follow = True
            try:
                followers = Followers.objects.filter(user=profile_user).count()
            except Followers.DoesNotExist:
                followers = 0
            
            try:
                following = Followers.objects.filter(follower_id=profile_user.pk).count()
            except Followers.DoesNotExist:
                following = 0
            
            try:
                posts = Post.objects.filter(user=profile_user)
                posts = posts.order_by("-timestamp").all() 

            except Post.DoesNotExist:
                return render(request, "network/index.html",{
                    "not_exist": True,
                })
            try:
                user = User.objects.get(pk=int(profile_user.pk))
                follower = Followers.objects.get(user=user, unique = user.pk, follower_id=request.user.id)
                follow_button = False
            except Followers.DoesNotExist:
                follow_button = True
                    # Pagination
            page = request.GET.get('page')
            paginator = Paginator(posts, 10)

            try:
                post = paginator.page(page)
            except PageNotAnInteger:
                post = paginator.page(1)
            except EmptyPage:
                post = paginator.page(paginator.num_pages)

            return render(request, "network/profile.html", {
                "user": profile_user,
                "followers": followers,
                "following": following,
                "posts": post,
                "follow": follow,
                "follow_button": follow_button,
            })


def following(request):
    if not request.user.is_authenticated:
        try:
            posts = Post.objects.all()
            posts = posts.order_by("-timestamp").all() 
        except Post.DoesNotExist:
            return render(request, "network/index.html",{
                "not_exist": True,
            })
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(posts, 10)
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        return render(request, "network/index.html", {
            "posts": post,
        })

    else:
        try:
            all_posts_following = Followers.objects.filter(follower_id = request.user.id)
            post_set = set()
            for n in range(all_posts_following.count()):
                post_set.add(all_posts_following[n].unique)
            post_list = (list(post_set))
            posts = Post.objects.filter(user__in=post_list)
            posts = posts.order_by("-timestamp").all()
            if posts:
                no_post = False
            else:
                no_post = True
                # Pagination
            page = request.GET.get('page')
            paginator = Paginator(posts, 10)

            try:
                post = paginator.page(page)
            except PageNotAnInteger:
                post = paginator.page(1)
            except EmptyPage:
                post = paginator.page(paginator.num_pages)
        except Followers.DoesNotExist:
            no_post = True

        return render(request, "network/following.html", {
            "posts": post,
            "no_post": no_post,

        })


def post(request, post_id):
    
    try:
        post = Post.objects.filter(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "GET":
        serialized_data = serialize("json", post)
        serialized_data = json.loads(serialized_data)
        return JsonResponse(serialized_data, safe=False)
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        new_text = data["new_body"]
        edit_post = Post.objects.get(pk=post_id)
        edit_post.body = new_text
        edit_post.save()
        return HttpResponse(status=204)


def like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if request.method == "PUT":
        # If user already like the post 
        if Like.objects.filter(user=user, post=post).exists():
            like = Like.objects.get(user=user, post=post)
            like.delete()
            post.like -= 1
            post.save()
            return JsonResponse({'liked': False, 'count': post.like})

        # If is not:
        like = Like(user=user, post=post)
        like.save()
        post.like += 1
        post.save()
        return JsonResponse({'liked': True, 'count': post.like})

    return HttpResponse(status=204)
