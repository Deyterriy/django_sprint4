from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Category, Comment, User
from django.utils import timezone
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, ProfileForm, CommentForm
from django.db.models import Count


class HomePageView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            Post.objects.select_related(
                'author', 'category', 'location'
            ).filter(
                pub_date__lte=timezone.now(),
                is_published=True,
                category__is_published=True,
            )
        ).annotate(comment_count=Count('comment'))
        return queryset.order_by('-pub_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comment.select_related('author')
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category_list.html'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(
            Category, slug=category_slug, is_published=True
        )
        queryset = (
            category.posts.select_related(
                'author',
                'location',
            )
            .filter(is_published=True, pub_date__lte=timezone.now())
            .annotate(comment_count=Count('comment'))
            .order_by('-pub_date')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category.objects.values('id', 'title', 'description').filter(
                is_published=True
            ),
            slug=self.kwargs['category_slug'],
        )
        context['category'] = category
        return context


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile_list.html'
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs['username']
        self.author = get_object_or_404(User, username=username)
        return (
            super()
            .get_queryset()
            .filter(author=self.author)
            .annotate(comment_count=Count('comment'))
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user
        return reverse('blog:profile', kwargs={'username': username})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'

    def dispatch(self, request, *args, **kwargs):
        author = self.get_object().author
        if author != self.request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        self.post_data = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('blog:post_detail', kwargs={'pk': pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create_post.html'

    def dispatch(self, request, *args, **kwargs):
        author = self.get_object().author
        if author != self.request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        self.post_data = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        username = self.request.user
        return reverse('blog:profile', kwargs={'username': username})


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        username = self.request.user
        return reverse('blog:profile', kwargs={'username': username})


class CommentAddView(LoginRequiredMixin, CreateView):
    post_obj = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post_obj.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'id'
    template_name = 'blog/comment.html'
    post_data = None

    def dispatch(self, request, *args, **kwargs):
        author = self.get_object().author
        if author != self.request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        self.post_data = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.post_data.pk
        return reverse('blog:post_detail', kwargs={'pk': pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        author = self.get_object().author
        if author != self.request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        self.post_data = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})
