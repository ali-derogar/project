from django.http import Http404
from django.shortcuts import get_object_or_404 , redirect
from web.models import Article

class Fieldmixin():
    def dispatch(self , request , *args , **kwargs):
        self.fields = [
            'title',
            'descriptions',
            'slug',
            'category',
            'is_special',
            'thumbnail',
            'published',
            'status'
        ]
        if request.user.is_superuser:
            self.fields.append('author')

        return super().dispatch(request , *args , **kwargs)

class Accessmixin():
    def dispatch(self , request ,pk , *args , **kwargs):
        articlex = get_object_or_404(Article , pk = pk)
        if request.user.is_superuser or request.user.is_author and articlex.status in ['d' ,'b']:
            return super().dispatch(request ,pk, *args , **kwargs)
        else:
            raise Http404('شما نمی توانید به این صفحه دسترسی داشته باشید ')

class Accessdeletemixin():
    def dispatch(self , request , *args , **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request , *args , **kwargs)
        else:
            raise Http404('شما نمی توانید به این صفحه دسترسی داشته باشید ')

class Formvalidmixin():
    def form_valid(self , form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit = False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
            
        return super().form_valid(form)

class SimpleLoginRequierd():
    def dispatch(self , request , *args , **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request , *args , **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect("login")