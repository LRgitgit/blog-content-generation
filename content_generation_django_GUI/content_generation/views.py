from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import BlogArticle

def home(request):
    return HttpResponse("Welcome to the Blog!")

def article_list(request):
    articles = BlogArticle.objects.all()
    return render(request, 'articles_list.html', {'articles': articles})

def article_detail(request, slug):
    article = get_object_or_404(BlogArticle, slug=slug)
    return render(request, 'article_detail.html', {'article': article})
