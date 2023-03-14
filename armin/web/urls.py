from django.urls import URLPattern, path , include
from .views import Article_list , Article_detail , Category_list , User_list , Search_list , Introduce_list , email_view


app_name = 'web'
urlpatterns = [
    path('',Introduce_list.as_view() , name= 'introduce'),
    path('email',email_view.as_view() , name= 'email'),
    path('article',Article_list.as_view() , name= 'home'),
    path('article/page/<int:page>',Article_list.as_view() , name= 'home'),
    path('article/<slug:slug>',Article_detail.as_view() , name='detail'),
    path('category/<slug:slug>',Category_list.as_view() , name='category'),
    path('category/<slug:slug>/page/<int:page>',Category_list.as_view() , name='category'),
    path('author/<slug:username>',User_list.as_view() , name='author'),
    path('author/<slug:username>/page/<int:page>',User_list.as_view() , name='author'),
    path('search/',Search_list.as_view() , name='search'),
    path('search/page/<int:page>',Search_list.as_view() , name='search'),

]