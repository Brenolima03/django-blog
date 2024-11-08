from typing import Any
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models import Q
from blog.models import Post, Page

PER_PAGE = 9

class PostListView(ListView):
  template_name = "blog/pages/index.html"
  context_object_name = "posts"
  paginate_by = PER_PAGE
  queryset = Post.objects.get_published()

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update({
      "page_title": "Home - "
    })
    return context

def paginate_queryset(request, queryset):
  paginator = Paginator(queryset, PER_PAGE)
  page_number = request.GET.get("page")
  return paginator.get_page(page_number)

class CreatedByListView(PostListView):
  def __init__(self, **kwargs: Any) -> None:
    super().__init__(**kwargs)
    self._temp_context: dict[str, Any] = {}

  def get_context_data(self, **kwargs) -> dict[str, Any]:
    ctx = super().get_context_data(**kwargs)
    user_full_name = self.user.username

    if self.user.first_name:
      user_full_name = f'{self.user.first_name} {self.user.last_name}'
    page_title = 'Posts de ' + user_full_name + ' - '
    ctx.update({
      'page_title': page_title,
    })
    return ctx

  def get_queryset(self) -> QuerySet[Any]:
    qs = super().get_queryset()
    qs = qs.filter(created_by__pk=self.user.pk)
    return qs

  def get(self, request, *args, **kwargs):
    self.author_pk = self.kwargs.get('author_pk')
    self.user = get_object_or_404(User, pk=self.author_pk)
    return super().get(request, *args, **kwargs)

class CategoryListView(PostListView):
  allow_empty = False

  def get_queryset(self) -> QuerySet[Any]:
    return super().get_queryset().filter(
      category__slug=self.kwargs.get("slug")
    )

  def get_context_data(self, **kwargs) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    page_title = f"{self.object_list[0].category.name} - Category - "
    context.update({
      "page_title": page_title
    })
    return context

class TagListView(PostListView):
  allow_empty = False

  def get_queryset(self) -> QuerySet[Any]:
    # Filter posts by the specific tag slug from the URL
    return super().get_queryset().filter(
      tags__slug=self.kwargs.get("slug")
    )

  def get_context_data(self, **kwargs) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    
    # Extract the tag name from the first post's tags in the filtered queryset
    first_post = self.object_list.first()
    tag_name = (
      first_post.tags.filter(slug=self.kwargs.get("slug")).first().name
      if first_post else "Unknown Tag"
    )
    
    # Set the page title
    page_title = f"{tag_name} - Tag - "
    context.update({
      "page_title": page_title
    })
    return context

class SearchListView(PostListView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._search_value = ""

  def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
    self._search_value = request.GET.get("search", "").strip()
    return super().setup(request, *args, **kwargs)

  def get_queryset(self) -> QuerySet[Any]:
    search_value = self._search_value

    return super().get_queryset().filter(
      Q(title__icontains=search_value) |
      Q(excerpt__icontains=search_value) |
      Q(content__icontains=search_value) |
      Q(tags__name__icontains=search_value)
    ).distinct()[:PER_PAGE]

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    search_value = self._search_value
    context.update({
      "page_title": f"{search_value[:30]} - Search - ",
      "search_value": search_value
    })
    return context

  def get(self, request, *args, **kwargs):
    if self._search_value == "":
      return redirect("blog:index")
    return super().get(request, *args, **kwargs)

class PageDetailView(DetailView):
  model = Page
  template_name = "blog/pages/page.html"
  slug_field = "slug"
  context_object_name = "page"

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    page = self.get_object()
    page_title = f"{page.title} - Page - "
    context.update({
      "page_title": page_title
    })
    return context

  def get_queryset(self) -> QuerySet[Any]:
    return super().get_queryset().filter(is_published=True)

class PostDetailView(DetailView):
  model = Post
  template_name = "blog/pages/post.html"
  slug_field = "slug"
  context_object_name = "post"

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    post = self.get_object()
    page_title = f"{post.title} - Post - "
    context.update({
      "page_title": page_title
    })
    return context

  def get_queryset(self) -> QuerySet[Any]:
    return super().get_queryset().filter(is_published=True)
