from django.shortcuts import render, redirect, get_object_or_404
from . models import Article, Category, Comment
from taggit.models import Tag
from . forms import AddArticleForm
from django.db.models import Count
import logging

logger = logging.getLogger(__name__)

def blog_home(request):
    all_articles = Article.objects.filter(status="published", active=True)
    featured =Article.objects.filter(status ="published", active=True, featured=True).latest("pub_date")
    
    context = {
        "articles":all_articles,
        "featured":featured,        
    }
    logger.info("Request for blog home page")
    return render(request, "blog/blog_home_new.html", context)

def blog_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    categories = Category.objects.all().annotate(articles_count=Count('article'))
    comments = article.comments.filter(active=True)

    context = {
        'article':article,
        'categories':categories,
        'comments':comments,
    }
    return render(request, 'blog/blog_detail.html', context)


def blog_category(request, slug):
    category = get_object_or_404(Category,slug=slug)
    all_articles = Article.objects.filter(status="published", active=True)
    category_articles = all_articles.filter(category=category)
    
    context = { "slug":slug,
               "articles":category_articles,}
    
    return render(request, 'blog/blog_category.html', context)

def blog_tag(request,slug):
    tag = get_object_or_404(Tag,slug=slug)
    articles = Article.objects.filter(tags = tag)
    context = {
        "tag":tag,
        "articles":articles
    }
    return render(request,"blog/blog_tag.html",context)




