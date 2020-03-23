from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from post.models import Post
import math


@login_required(redirect_field_name='next', login_url=reverse_lazy('login'))
def post(request, pid):
    try:
        p = Post.objects.get(pk=pid)
        return render(request, 'posts/post.html',
                      context={'title': p.title, 'content': p.content, 'description': p.description,
                               'date': p.date, 'author': p.author.name})
    except Post.DoesNotExist:
        return HttpResponseNotFound()


@login_required(redirect_field_name='next', login_url=reverse_lazy('login'))
def posts_table(request):
    try:
        page = request.GET.get('page', '1')
        p = int(page)
    except ValueError:
        p = 1
    total = Post.objects.count()
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
        context['posts'] = Post.objects.all()[st:ed]
        return render(request, 'posts/posttable.html', context=context)
