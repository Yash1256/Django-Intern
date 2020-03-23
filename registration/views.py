import math

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from .forms import AuthorForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from .models import Author
from post.models import Post


class Landing(View):
    def get(self, request):
        return render(request, 'registration/index.html')


class Register(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        a = AuthorForm(request.POST)
        try:
            if a.is_valid():
                a.save()
                return redirect('login')
            else:
                return render(request, 'registration/register.html', context={'error': a.errors})
        except ValidationError as V:
            return render(request, 'registration/register.html', context={'error': V.message_dict})


class Login(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        if email is None or password is None:
            return render(request, 'registration/login.html', context={'error': 'Fields are required.'})
        u = authenticate(request, email=email, password=password)
        if u is None:
            return render(request, 'registration/login.html', context={'error': 'Email or Password is not valid.'})
        else:
            login(request, u)
            if request.GET.get('next', None):
                return redirect(reverse(request.GET.get('next')))
            else:
                a = Author.objects.get(email=u.email)
                return redirect('author', a.pk)


@login_required(redirect_field_name='next', login_url=reverse_lazy('login'))
def author(request, aid):
    try:
        a = Author.objects.get(pk=aid)
        return render(request, 'registration/author.html',
                      context={'count': Post.objects.filter(author_id=a.pk).count(), 'bdate': a.birthdate,
                               'name': a.name})
    except Author.DoesNotExist:
        return HttpResponseNotFound()


@login_required(redirect_field_name='next', login_url=reverse_lazy('login'))
def authors_table(request):
    try:
        page = request.GET.get('page', '1')
        p = int(page)
    except ValueError:
        p = 1
    total = Author.objects.count()
    count = math.ceil(total/10)
    context = dict()
    if count < p:
        return HttpResponseNotFound()
    else:
        if p > 1:
            context['prev'] = p - 1
        if count > p:
            context['next'] = p + 1
        if p > 2:
            context['prev_pg'] = []
            for i in range(p-2, 0, -1):
                context['prev_pg'].append(i)
                if len(context['prev_pg']) > 2:
                    context['prev_pg'] = context['prev_pg'][:2]
                    context['ellipsisP'] = True
        if count > p + 1:
            context['next_pg'] = []
            for i in range(p + 2, count + 1, 1):
                context['next_pg'].append(i)
                if len(context['next_pg']) > 2:
                    context['next_pg'] = context['next_pg'][:2]
                    context['ellipsisN'] = True
            context['next_pg'].reverse()
        st = (p-1)*10
        ed = min(p*10, total)
        context['page'] = p
        context['authors'] = Author.objects.all()[st:ed]
        return render(request, 'registration/authors.html', context=context)
