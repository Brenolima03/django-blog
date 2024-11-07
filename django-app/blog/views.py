from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import ListView
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
    # Use get_object_or_404 to fetch the user or raise 404 if not found
    self.user = get_object_or_404(User, pk=self.author_pk)
    return super().get(request, *args, **kwargs)

def category(request, slug):
  posts = Post.objects.get_published().filter(category__slug=slug)
  page_obj = paginate_queryset(request, posts)
  if not page_obj:
    raise Http404()
  page_title = f"{page_obj[0].category.name} - Category - "
  return render(
    request,
    "blog/pages/index.html",
    {
      "page_obj": page_obj,
      "page_title": page_title
    }
  )

def tag(request, slug):
  posts = Post.objects.get_published().filter(tags__slug=slug)
  page_obj = paginate_queryset(request, posts)
  if not page_obj:
    raise Http404()
  page_title = f"{page_obj[0].tags.first().name} - Tag - "
  return render(
    request,
    "blog/pages/index.html",
    {
      "page_obj": page_obj,
      "page_title": page_title
    }
  )

def search(request):
  search_value = request.GET.get("search", "").strip()
  if not search_value:
    return render(request, "blog/pages/index.html", {"page_obj": [], "search_value": search_value, "page_title": "Search - "})

  posts = (
    Post.objects.get_published()
    .filter(
      Q(title__icontains=search_value) |
      Q(excerpt__icontains=search_value) |
      Q(content__icontains=search_value) |
      Q(tags__name__icontains=search_value)
    )
    .distinct()
  )
  page_obj = paginate_queryset(request, posts)
  return render(
    request,
    "blog/pages/index.html",
    {
      "page_obj": page_obj,
      "search_value": search_value,
      "page_title": f"{search_value[:30]} - Search - "
    }
  )

def page(request, slug):
  page_obj = get_object_or_404(Page, is_published=True, slug=slug)
  page_title = f"{page_obj.title} - Page - "
  return render(
    request,
    "blog/pages/page.html",
    {
      "page": page_obj,
      "page_title": page_title
    }
  )

def post(request, slug):
  post_obj = get_object_or_404(Post, slug=slug)
  page_title = f"{post_obj.title} - Post - "
  return render(
    request,
    "blog/pages/post.html",
    {
      "post": post_obj,
      "page_title": page_title
    }
  )
