from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.


class PostsListView(ListView):
    template_name = "all_posts.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 4


class PostDetailView(DetailView):
    template_name = "post_detail.html"
    model = Post
    context_object_name = "post"

    def post(self, request, *args, **kwargs):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_mod = self.request.user.groups.filter(
            name="mod").exists() or self.request.user.is_staff
        is_blocked = self.request.user.groups.filter(
            name="blocked").exists()

        context['is_mod'] = is_mod
        context['is_blocked'] = is_blocked
        return context


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'posts.change_post'
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'posts.add_post'

    model = Post
    template_name = "post_form.html"
    success_url = '/'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
