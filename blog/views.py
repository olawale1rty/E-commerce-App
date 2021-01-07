from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from web.models import (SiteDetail, Categorie, Order, SearchQuery)
from web.forms import SubscribeForm
from web.views import auto_paginate
from blog.models import Article
from blog.models import Comment as Cmt
from blog.models import Categorie as BlogCategory
from blog.forms import CommentForm

# Create your views here.
class Blog(View):

    def get(self, request):
        context = {}
        articles_list = Article.objects.all().filter(
            publication_status  = 'publish').order_by('-upload_date')
        context['articles'] = auto_paginate(request=request,
            queryset = articles_list , paginate_by = 4)
        context['subscribeform'] = SubscribeForm()
        context['active_blog'] = True
        context['blog_categories'] = BlogCategory.objects.all()
        context['site_details'] = SiteDetail.objects.get()
        context['categories'] = Categorie.objects.all()
        try:
            order = Order.objects.filter(user=request.user, ordered=False)
            if order.exists():
                context['cart'] = order[0]
            else:
                context['cart'] = order
        except: 
            pass
        template = 'blog/blog.html'
        return render(request, template, context)

class BlogArticle(View):

    def get(self, request, ** kwargs):
        template = 'blog/blog-detail.html'
        context = {}
        default_article = Article.objects.get(slug = kwargs['slug'])
        default_value = {'article': default_article}
        try:
            context['form_status'] = kwargs['form_status']
        except:
            pass
        context['subscribeform'] = SubscribeForm()
        context['comment_form'] = CommentForm( initial = default_value)
        context['comments'] = Cmt.objects.filter(
            article = default_article).order_by('-upload_timestamp')
        context['active_blog'] = True
        context['article'] = Article.objects.get(slug = kwargs['slug'])
        context['site_details'] = SiteDetail.objects.get()
        context['blog_categories'] = BlogCategory.objects.all()
        try:
            order = Order.objects.filter(user=request.user, ordered=False)
            if order.exists():
                context['cart'] = order[0]
            else:
                context['cart'] = order
        except: 
            pass
        context['categories'] = Categorie.objects.all()
        return render(request, template, context)

class BlogArticleCategory(View):

    def get(self, request, ** kwargs):
        context = {}
        fetch_category = kwargs['category']
        fetch_category = BlogCategory.objects.get(article_category = fetch_category)
        articles_list = Article.objects.all().filter(
            publication_status  = 'publish', categories = fetch_category).order_by('-upload_date')
        context['articles'] = auto_paginate(request=request,
            queryset = articles_list , paginate_by = 4)
        context['subscribeform'] = SubscribeForm()
        context['site_details'] = SiteDetail.objects.get()
        context['current_category'] = fetch_category
        context['blog_categories'] = BlogCategory.objects.all()
        context['categories'] = Categorie.objects.all()
        try:
            order = Order.objects.filter(user=request.user, ordered=False)
            if order.exists():
                context['cart'] = order[0]
            else:
                context['cart'] = order
        except: 
            pass
        template = 'blog/blog.html'
        return render(request, template, context)

class Comment(View):

    def post(self, request):
        new_comment = CommentForm(request.POST)
        if(new_comment.is_valid()):
            new_comment.save()
            return BlogArticle().get(request,
             slug = new_comment.cleaned_data['article'].slug,
             form_status = 'success')
        else:
            return BlogArticle().get(request,
             slug = new_comment.cleaned_data['article'].slug,
             form_status = 'fail')

def search_view(request):
    query = request.GET.get('q', None)
    user = None
    context = {}
    try:
        order = Order.objects.filter(user=request.user, ordered=False)
        if order.exists():
            context['cart'] = order[0]
        else:
            context['cart'] = order
    except: 
        pass
    if request.user.is_authenticated:
        user = request.user
    context["query"] = query
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        blog_list = Article.objects.search(query=query).filter(
            publication_status  = 'publish').order_by('-upload_date')
        context['blog_list'] = auto_paginate(request=request,
            queryset = blog_list , paginate_by = 4)
    context['subscribeform'] = SubscribeForm()
    context['site_details'] = SiteDetail.objects.get()
    context['blog_categories'] = BlogCategory.objects.all()
    context['categories'] = Categorie.objects.all()
    context['active_blog'] = True
    return render(request, 'blog/view.html',context)