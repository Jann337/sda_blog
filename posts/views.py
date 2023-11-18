from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group

# Create your views here.


def all_posts(request):
    posts = Post.objects.all()
    print(request.user)

    return render(request, "all_posts.html", context={"posts": posts})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    is_mod = request.user.groups.filter(
        name="mod").exists() or request.user.is_staff
    is_blocked = request.user.groups.filter(
        name="blocked").exists()

    if request.method == "POST":
        delete_id = request.POST.get('delete')
        author_to_ban = request.POST.get('block')

        if delete_id:
            post_to_delete = Post.objects.get(pk=delete_id)
            post_to_delete.delete()

        if author_to_ban:
            author = User.objects.filter(
                username=author_to_ban).first()
            mod_group = Group.objects.get(name='mod')
            default_group = Group.objects.get(name='default')
            blocked_group = Group.objects.get(name='blocked')

            mod_group.user_set.remove(author)
            default_group.user_set.remove(author)
            blocked_group.user_set.add(author)

        return redirect('home')

    return render(request, "post_detail.html", context={"post": post, "is_mod": is_mod, "is_blocked": is_blocked})


@permission_required('posts.change_post', raise_exception=True)
@login_required
def post_update(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.body = request.POST.get("body")
        post.author = request.user
        post.save()

        return redirect("post_detail", pk=post.pk)

    return render(request, "edit_post.html", context={"post": post})


@permission_required('posts.add_post', raise_exception=True)
@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        author = request.user
        post = Post.objects.create(title=title,
                                   body=body,
                                   author=author)
        post.save()

        return redirect("home")

    return render(request, "create_post.html")
