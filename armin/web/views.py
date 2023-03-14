from ipaddress import ip_address
from multiprocessing import context
from re import template
from urllib import request
from django.shortcuts import get_object_or_404, render , redirect
from accont.models import User
from .models import Article, Articlehit, Category, Introduce, Email_Saver
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView , CreateView
from django.db.models import Q
from django.contrib import messages


class Introduce_list(ListView):
    template_name = 'web/introduce.html'
    queryset = Introduce.objects.all()


class Article_list(ListView):
    paginate_by = 4
    template_name = 'web/article_list.html'
    queryset = Article.objects.publish()


class Article_detail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug, status='p')

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        return article


class Category_list(ListView):
    paginate_by = 2
    template_name = 'web/category_list.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        global cat
        cat = get_object_or_404(Category, slug=slug, status=True)
        return cat.article_category.publish()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = cat
        return context


class User_list(ListView):
    template_name = 'web/user_list.html'
    paginate_by = 2

    def get_queryset(self):
        username = self.kwargs.get('username')
        global cat
        cat = get_object_or_404(User, username=username)
        return cat.article.publish()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = cat
        return context


class Search_list(ListView):
    template_name = 'web/search_list.html'
    paginate_by = 2

    def get_queryset(self):
        global search
        search = self.request.GET.get('q')
        return Article.objects.filter((Q(descriptions__icontains=search) | Q(title__icontains=search)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = search
        return context


class email_view(CreateView):
    model = Email_Saver
    fields = ["email"]
    template_name = "web/email.html"

