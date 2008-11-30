from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify

from models import News
from forms import NewsForm

def show_all(request, offset=0, number=10, template="news/latest.html"):
    offset = int(offset)
    number = int(number)
    offset_step = offset * number
    news_count = News.objects.all().count()
    newscount = news_count // number
    if news_count % number:
        newscount += 1
    page = {
            "offset": offset,
            "number": number,
            "offset_step": offset_step,
            "newsrange": range(newscount) if newscount is not 1 else [],
            }
    n = News.objects.all()[offset_step:offset_step+number]
    return render_to_response(template, {
        "news": n,
        "page": page,
        }, context_instance=RequestContext(request))

def latest(request, offset=0, number=10, template="news/latest.html"):
    offset = int(offset)
    number = int(number)
    offset_step = offset * number
    news_count = News.objects.all().count()
    newscount = news_count // number
    if news_count % number:
        newscount += 1
    page = {
            "offset": offset,
            "number": number,
            "offset_step": offset_step,
            "newsrange": range(newscount) if newscount is not 1 else [],
            }
    n = News.objects.exclude(show=False)[offset_step:offset_step+number]
    return render_to_response(template, {
        "news": n,
        "page": page,
        }, context_instance=RequestContext(request))

def details(request, slug, template="news/details.html"):
    n = get_object_or_404(News, slug=slug)
    return render_to_response(template, {
        "news": n,
        }, context_instance=RequestContext(request))

@login_required
def create(request, template="news/create.html"):
    def get_slug(text, numb=0):
        "Create unique slug"
        if numb:
            text += "_%d" % numb
        s = slugify(text)
        try:
            News.objects.get(slug=s)
            return get_slug(text, numb + 1)
        except News.DoesNotExist:
            pass
        return s
    u = request.user
    if request.POST:
        n = News(author=u, show=False, slug=get_slug(request.POST['title']))
        f = NewsForm(request.POST, instance=n)
        if f.is_valid():
            n = f.save()
            return HttpResponseRedirect(n.get_absolute_url() + "show/")
    else:
        f = NewsForm()
    return render_to_response(template, {
        "form": f,
        }, context_instance=RequestContext(request))


@login_required
def edit(request, slug, template="news/create.html"):
    n = get_object_or_404(News, slug=slug)
    u = request.user
    if not (u is n.author or u.has_perm("news.can_edit")):
        return HttpResponseRedirect(request.META['HTTP_REFERER'] or "/news/")
    if request.POST:
        f = NewsForm(request.POST, instance=n)
        if f.is_valid():
            n = f.save()
            return HttpResponseRedirect(n.get_absolute_url() + "show/")
    else:
        f = NewsForm(instance=n)
    return render_to_response(template, {
        "form": f,
        }, context_instance=RequestContext(request))

@login_required
def delete(request, slug):
    n = get_object_or_404(News, slug=slug)
    u = request.user
    if u is n.author or u.has_perm("news.can_delete"):
        n.delete()
    return HttpResponseRedirect("/news/")


@login_required
def confirm(request, slug):
    u = request.user
    n = get_object_or_404(News, slug=slug)
    if u.has_perm("news.can_edit"):
        n.show = True
        n.save()
    return HttpResponseRedirect(n.get_absolute_url() + "show/")
