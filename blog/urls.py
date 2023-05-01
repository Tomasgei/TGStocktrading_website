from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('',views.blog_home, name="blog_home" ),
    #path('add', views.blog_add_article, name="add_article"), 
    path('<slug:slug>', views.blog_detail, name="blog_detail"),
    path('category/<str:slug>/', views.blog_category, name="blog_category"), 
    path('tag/<str:slug>/', views.blog_tag, name="blog_tag"),   
]
