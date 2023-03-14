from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes , force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
# oder sections
from accont.models import User
from .forms import Profileform
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from web.models import Article
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView , PasswordChangeView
from .mixin import (
                    Fieldmixin,
                    Formvalidmixin,
                    Accessmixin,
                    Accessdeletemixin,
                    SimpleLoginRequierd
)
from django.views.generic import (
                    ListView ,
                    CreateView ,
                    UpdateView ,
                    DeleteView ,
                    DetailView
) 

class Article_list(SimpleLoginRequierd ,ListView):
    template_name = 'registration/home.html'
    paginate_by: 12
    def get_queryset(self):
        if self.request.user.is_superuser:
            x = Article.objects.all()
        else:
            x = Article.objects.filter(author = self.request.user)
        return x

class Detail_preview(DetailView):
    template_name = 'registration/detail_preview.html'
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404( Article , slug = slug , status='d')

class Article_create(Fieldmixin,SimpleLoginRequierd , Formvalidmixin,CreateView):
    template_name = 'registration/create_article.html'
    model = Article

class Article_update(Fieldmixin, Accessmixin , Formvalidmixin,UpdateView):
    template_name = 'registration/update_article.html'
    model = Article

class Article_delete(Accessdeletemixin, DeleteView):
    template_name = 'registration/delete_article.html'
    model = Article
    success_url = reverse_lazy("account:home")

class Profile(LoginRequiredMixin ,UpdateView):
    template_name = 'registration/profile.html'
    success_url = reverse_lazy("account:profile")
    form_class = Profileform
    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)
    def get_form_kwargs(self):
        kwargs = super(Profile,self).get_form_kwargs()
        kwargs.update({
            'user':self.request.user
        })
        return kwargs

class Login(LoginView):
    def get_success_url(self):
        if self.request.user.is_superuser or self.request.user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')
# register with email section 
class Register(CreateView):
    template_name = "registration/email_login.html"
    form_class = SignupForm
    def form_valid(self ,form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت با ایمیل'
        message = render_to_string('registration/email_account_activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('برای ادامه فرآیند ثبت نام ایمیل خود را بررسی کنید  <a href="/login">ورود</a>')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        return HttpResponse('ممنون از ثبت نام شما ... برای لاگین <a href="/login">کلیک کنید</a> ')
    else:
        return HttpResponse('لینک منقضی شده است ... <a href="/account/register">کلیک کنید</a>')
