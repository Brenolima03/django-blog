from django.urls import path
from blog.views import category, index, page, post, created_by

app_name = 'blog'

urlpatterns = [
  path('', index, name='index'),
  path('post/<slug:slug>/', post, name='post'),
  path('page/', page, name='page'),
  path('created_by/<int:author_pk>/', created_by, name='created_by'),
  path('created_by/<slug:slug>/', category, name='category'),
]
