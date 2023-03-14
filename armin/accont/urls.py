from django.urls import path, re_path
from accont.views import (
    Article_list ,
    Article_create ,
    Article_update ,
    Article_delete ,
    Detail_preview ,
    Profile ,
    Register,
    activate,
)

app_name = 'account'

urlpatterns = [
    path('',Article_list.as_view() , name= 'home'),
    path('article-create/',Article_create.as_view() , name= 'article_create'),
    path('Article-delete/<int:pk>',Article_delete.as_view() , name= 'article_delete'),
    path('article-update/<int:pk>',Article_update.as_view() , name= 'article_update'),
    path('detail-preview/<slug:slug>',Detail_preview.as_view() , name= 'detail_preview'),
    path('profile/*',Profile.as_view() , name= 'profile'),
    path("register/", Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
]
