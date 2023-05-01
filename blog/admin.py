from django.contrib import admin
from . models import Article,Category,Comment,IpModel

# Register your models here.
admin.site.register(Category)
admin.site.register(IpModel)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'pub_date','updated','active','status')
    list_filter = ('author', 'pub_date','active','status')
    search_fields = ('author', 'title', 'active')
    actions = ['approve_article',
               'ban_article',
               "publish_article",
               'to_draft_article',]

    def approve_article(self, request, queryset):
        queryset.update(active=True)
    
    def ban_article(self, request, queryset):
        queryset.update(active=False)
        
    def publish_article(self, request, queryset):
        queryset.update(status="published")
    
    def to_draft_article(self, request, queryset):
        queryset.update(status="draft")
    
        
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('author', 'article', 'active')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        
    
