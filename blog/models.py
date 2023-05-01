from django.db import models
from taggit.managers import TaggableManager
from django.urls import reverse
from autoslug import AutoSlugField

from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = AutoSlugField(populate_from = "title")
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

class IpModel(models.Model):
    ip = models.CharField(max_length=100)

class Article(models.Model):
    
    options = (
        ("draft","Draft"),
        ("published","Published"),
        
    )
    
    title = models.CharField(max_length=255)
    premium = models.BooleanField(default=False, verbose_name='Premium content')
    pub_date = models.DateField(auto_now=True, editable=True, verbose_name="Published date")
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from = "title", unique_with="pub_date__month")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=options, default="draft")
    active = models.BooleanField(default=False)
    tags = TaggableManager()
    category = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False, verbose_name='Featured article')
    image = models.ImageField(null=True, blank=True, upload_to="images/") 
    content = models.TextField()
    favourites = models.ManyToManyField(User,related_name="favourite",default=None, blank=True)
    likes = models.ManyToManyField(User,related_name="like", default=None, blank = True)
    like_count = models.BigIntegerField(default=0)
    #views = models.ManyToManyField(IpModel, related_name="post_views", blank=True)
    #likes = models.ManyToManyField(User, related_name="article")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:blog_detail", kwargs={"slug": self.slug})

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["created"]
        
    def __str__(self):
        return self.article.title
    
    
    


