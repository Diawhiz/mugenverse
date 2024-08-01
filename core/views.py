from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from django.views import generic
from .forms import CommentForm


# Create your views here.
class HomeView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-posted_on')
    template_name = 'core/post_list.html'
    context_object_name = 'home_view'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        recent_posts = Post.objects.all().order_by('-posted_on')[:5]
        context['recent_posts'] = recent_posts
        return context

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'core/post_detail.html'
    context_object_name = 'post_detail'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Post, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.filter(active=True)
        comment_form = CommentForm()
        recent_posts = Post.objects.all().order_by('-posted_on')[:5]
        context['categories'] = Category.objects.all()
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['recent_posts'] = recent_posts
        return context
    

def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', slug=post.slug)
    return render(request, 'core/post_detail.html', {'post': post, 'comment_form': comment_form})


class CategoryView(generic.ListView):
    model = Post
    template_name = 'core/category_posts.html'
    context_object_name = 'category_view'
    paginate_by = 30

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = Category.objects.get(slug=category_slug)
        return Post.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categor_slug = self.kwargs['category_slug']
        category = Category.objects.get(slug=categor_slug)
        recent_posts = Post.objects.all().order_by('-posted_on')[:5]
        context['categories'] = Category.objects.all()
        context['category'] = category
        context['recent_posts'] = recent_posts
        return context
    
#The code below is for search field
class SearchResultsView(generic.ListView):
    model = Post
    template_name = 'core/search_results.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if search_query:
            return Post.objects.filter(title__icontains=query)
        return Post.objects.all()
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(*kwargs)
    #     csrf_token = get_token(self.request)
    #     context['csrf_token'] = csrf_token
    #     return context
    
    # def post(self, request, *args, **kwargs):
    #     csrf_token = self.request.POST.get('csrfmiddlewaretoken')
    #     query = self.request.POST.get('q')
    #     results = Post.objects.filter(title__icontains=query)
    #     #return super().post(request, *args, **kwargs)
    #     return render(request, 'core/search_results.html', {'results': results})
