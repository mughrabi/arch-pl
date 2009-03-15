# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.http import Http404
from django.views.decorators.cache import cache_page

import json
import markdown

from models import Thread, Post
from forms import PostForm, ThreadForm, AdvancedSearchForm


@login_required
@user_passes_test(lambda u: u.has_perm("forum.thread.can_change"))
def block_thread(request, thread_slug):
    "Block any single thread"
    t = get_object_or_404(Thread, slug=thread_slug)
    t.closed = not t.closed
    t.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'] or "/forum/")

def thread_list(request, offset_step=0, number=20, popupinfo=None):
    offset_step = int(offset_step)
    number = int(number)
    offset = offset_step * number
    u = request.user
    threads = Thread.objects.all()[offset:offset + number]
    # template data
    pageinfo = {
            "offset": offset,
            "number": number,
            "offset_step": offset_step,
            "next": offset_step + 1,
            }
    return render_to_response("forum/thread_list.html", {
        "threads": threads,
        "page": pageinfo,
        "popupinfo": popupinfo,
        }, context_instance=RequestContext(request))

def thread(request, thread_slug, offset_step=None, number=20,
        template="forum/thread.html"):
    # ++thread.count
    t = get_object_or_404(Thread, slug=thread_slug)
    t.view_count += 1
    t.save()
    if offset_step:
        offset_step = int(offset_step)
        offset = offset_step * number
    else:
        offset = t.post_count - number
        if offset < 0:
            offset = 0
        offset_step = t.post_count // number
    number = int(number)
    p = t.post_set.all()[offset:offset+number]
    f = PostForm()

    sitecount = t.post_count // number
    if sitecount and t.post_count % number:
        sitecount += 1
    pageinfo = {
            "offset": offset,
            "number": number,
            "offset_step": offset_step,
            "sitecount": range(sitecount),
            }
    return render_to_response(template, {
        "thread": t,
        "post": p,
        "form": f,
        "page": pageinfo,
        }, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm("forum.add_post"))
def add_post(request, thread_slug, post_id=None,
        template="forum/add_post.html"):
    "Add new post"
    t = get_object_or_404(Thread, slug=thread_slug)
    u = request.user
    if t.closed:
        return HttpResponseRedirect(t.get_absolute_url())
    if t.latest_post.author == u:
        return edit_post(request, thread_slug, t.latest_post.id)
        #return HttpResponseRedirect(t.get_absolute_url())
    if request.POST:
        p = Post(thread=t, author=u)
        f = PostForm(request.POST, instance=p)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(t.get_absolute_url())
    else:
        data = {}
        if post_id:
            q_post = t.post_set.get(id=post_id)
            q_info = u">**%s powiedział:**\n>" % q_post.author.username
            q_info = [q_info, ]
            q_msg = [l for l in q_post.text.split("\n")]
            data['text'] = "\n> ".join(q_info + q_msg) + "\n\n"
        f = PostForm(data)
    return render_to_response(template, {
        "topic": t,
        "form": f,
        }, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm("forum.add_thread"))
@user_passes_test(lambda u: u.has_perm("forum.add_post"))
def add_thread(request, template="forum/add_thread.html"):
    "Create new thread and first post"
    def get_slug(text, numb=0):
        "Create unique slug"
        text = text[:110]
        if numb:
            text = text.rsplit("_", 1)[0] + "_%d" % numb
        s = slugify(text)
        if Thread.objects.filter(slug=s).count():
            return get_slug(text, numb + 1)
        return s
    u = request.user
    tf = ThreadForm()
    pf = PostForm()
    if request.POST:
        t = Thread(author=u, latest_post_author=u,
                slug=get_slug(request.POST['title']))
        tf = ThreadForm(request.POST, instance=t)
        if tf.is_valid():
            tfins = tf.save()
            p = Post(thread=tfins, author=u)
            pf = PostForm(request.POST, instance=p)
            if pf.is_valid():
                pfins = pf.save()
                return HttpResponseRedirect(tfins.get_absolute_url())
            else:
                tfins.delete()
    return render_to_response(template, {
        "t_form": tf,
        "p_form": pf,
        }, context_instance=RequestContext(request))


@login_required
def toggle_solved(request, thread_slug):
    "Toggle any single thread as solved"
    t = get_object_or_404(Thread, slug=thread_slug)
    if t.author == request.user or request.user.has_perm("thread.can_edit"):
        t.solved = not t.solved
        t.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'] or "/forum/")
    #return thread_list(request,
    #        popupinfo="Post oznaczony został jako *Rozwiązany*")

@login_required
@user_passes_test(lambda u: u.has_perm("forum.can_change"))
def toggle_sticky(request, thread_slug):
    "Toggle any single thread sticky"
    t = get_object_or_404(Thread, slug=thread_slug)
    t.sticky = not t.sticky
    t.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'] or "/forum/")

@login_required
@user_passes_test(lambda u: u.has_perm("forum.add_post"))
def edit_post(request, thread_slug, post_id, template="forum/add_post.html"):
    t = get_object_or_404(Thread, slug=thread_slug)
    p = t.post_set.get(id=post_id)
    u = request.user
    if not u.has_perm("thread.can_edit") and not \
            (t.latest_post.id == p.id and p.author == u):
        return HttpResponseRedirect(t.get_absolute_url())
    if request.POST:
        f = PostForm(request.POST, instance=p)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(t.get_absolute_url())
    f = PostForm(instance=p)
    return render_to_response(template, {
        "topic": t,
        "form": f,
        }, context_instance=RequestContext(request))

@login_required
def delete_post(request, thread_slug, post_id):
    t = get_object_or_404(Thread, slug=thread_slug)
    p = t.post_set.get(id=post_id)
    u = request.user
    if u.has_perm("thread.can_delete") or \
            (t.latest_post.id == p.id and p.author == u):
        p.delete()
        if not t.post_set.count():
            return HttpResponseRedirect("/forum/")
    return HttpResponseRedirect(t.get_absolute_url())

def quick_search(request, searchtext=None, template="forum/thread_list.html"):
    pageinfo = { "sitecount" : [] }
    if request.GET:
        searchtext = request.GET.get("searchtext")
    if not searchtext or \
            len(searchtext.replace(" ", "")) < len(searchtext.split()) * 4:
        return thread_list(request,
                popupinfo="podana fraza składa się ze zbyt krótkich haseł")
    thread = Thread.objects.filter(
            Q(post__text__contains=searchtext) | Q(title__contains=searchtext)
            ).distinct()[:20]
    return render_to_response(template, {
        "old_threads": thread,
        "page": pageinfo,
        }, context_instance=RequestContext(request))

def advanced_search(request, template="forum/advanced_search.html"):
    t = None
    if request.GET:
        f = AdvancedSearchForm(request.GET)
        if f.is_valid():
            t = Thread.objects.all()
            if f.cleaned_data['searchtext']:
                stext = f.cleaned_data['searchtext']
                t = t.filter(Q(post__text__contains=stext) | Q(title__contains=stext))
            if f.cleaned_data['user']:
                t = t.filter(post__author__username__exact=f.cleaned_data['user'])
            if f.cleaned_data['solved']:
                t = t.filter(solved=True)
            t = t.distinct()[:30]
    else:
        f = AdvancedSearchForm()
    return render_to_response(template, {
        "threads": t,
        "form": f,
        }, context_instance=RequestContext(request))

@login_required
def user_latest_active_threads(request, template="forum/thread_list.html"):
    t = Thread.objects.filter(post__author=request.user)[:10].distinct()
    return render_to_response(template, {
        "old_threads": t,
        "page": { "sitecount" : [] },
        }, context_instance=RequestContext(request))

@login_required
def delete_thread(request, thread_slug):
    if not request.user.has_perm("forum.thread.can_delete"):
        return HttpResponseRedirect(request.META['HTTP_REFERER'] or "/forum/")
    t = get_object_or_404(Thread, slug=thread_slug)
    t.delete()
    return HttpResponseRedirect("/forum/")

@login_required
def text_to_markdown(request):
    if request.is_ajax():
        resp = {}
        resp['text'] = request.POST.get('text', '')
        resp['markdown'] = markdown.markdown(resp['text'])
        return HttpResponse(json.dumps(resp), mimetype='application/javascript')
    return Http404
