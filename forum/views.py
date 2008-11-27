# -*- coding: utf-8 -*-

import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.db.models import Q

from settings import FORUM_MAX_DAY_MARK
from models import Thread, Post
from models import VisitedThread, AllVisited
from forms import PostForm, ThreadForm, AdvancedSearchForm

def thread_list(request, offset_step=0, number=20,
        template="forum/thread_list.html"):
    offset_step = int(offset_step)
    number = int(number)
    offset = offset_step * number
    # fetch from database
    u = request.user
    # if possible, mark threads containing new messages
    if u.is_authenticated():
        dt = datetime.datetime.now() - datetime.timedelta(FORUM_MAX_DAY_MARK)
        try:
            allcv = AllVisited.objects.get(user=u)
            dt = dt if dt > allcv.date else allcv.date
        except AllVisited.DoesNotExist:
            pass
        if offset == 0:
            unreaded = list(Thread.objects.filter(
                    latest_post_date__gt=dt).exclude(visitedthread__user=u))
            for u in unreaded:
                u.is_new = True
        else:
            unreaded = []
        unreaded_offset = number - len(unreaded)
        threads = Thread.objects.all()[len(unreaded):unreaded_offset]
        # join unreaded and old threads lists
        thread = unreaded + list(threads)
    else:
        thread = Thread.objects.all()[offset:offset+number]
    # template data
    pageinfo = {
            "offset": offset,
            "number": number,
            "offset_step": offset_step,
            "sitecount": [],
            }
    return render_to_response(template, {
        "thread": thread,
        "page": pageinfo,
        }, context_instance=RequestContext(request))

def thread(request, thread_slug, offset_step=0, number=20,
        template="forum/thread.html"):
    offset_step = int(offset_step)
    number = int(number)
    offset = offset_step * number
    t = get_object_or_404(Thread, slug=thread_slug)
    t.view_count += 1
    t.save()
    p = t.post_set.all()[offset:offset+number]
    f = PostForm()
    if request.user.is_authenticated():
        vt, created = VisitedThread.objects.get_or_create(
                user=request.user, thread=t)
        vt.date = datetime.datetime.now()
        vt.save()
    # template data
    sitecount = t.post_count // number
    if t.post_count % number:
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
    t = get_object_or_404(Thread, slug=thread_slug)
    u = request.user
    if t.latest_post.author == u:
        return HttpResponseRedirect(t.get_absolute_url())
    if request.POST:
        f = PostForm(request.POST, instance=Post(thread=t, author=u))
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(t.get_absolute_url())
    else:
        data = {}
        if post_id:
            # TODO - add quote mark
            data['text'] = "> ".join(
                    t.post_set.get(id=post_id).text.split("\n"))
        f = PostForm(data)
    return render_to_response(template, {
        "topic": t,
        "form": f,
        }, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm("forum.add_thread"))
@user_passes_test(lambda u: u.has_perm("forum.add_post"))
def add_thread(request, template="forum/add_thread.html"):
    def get_slug(text, numb=0):
        "Create unique slug"
        if numb:
            text += "_%d" % numb
        s = slugify(text)
        if Thread.objects.filter(slug=s).count():
            return get_slug(text, numb + 1)
        return s
    u = request.user
    if request.POST:
        t = Thread(author=u, slug=get_slug(request.POST['title']))
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
    else:
        tf = ThreadForm()
        pf = PostForm()
    return render_to_response(template, {
        "t_form": tf,
        "p_form": pf,
        }, context_instance=RequestContext(request))


@login_required
def mark_all_read(request):
    "Create global `readed` mark"
    u = request.user
    VisitedThread.objects.filter(user=u).delete()
    obj, created = AllVisited.objects.get_or_create(user=u)
    if not created:
        obj.date = datetime.datetime.now()
        obj.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'] or "/forum/")

@login_required
def toggle_solved(request, thread_slug):
    t = get_object_or_404(Thread, slug=thread_slug)
    if t.author == request.user:
        t.solved = not t.solved
        t.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'] or "/forum/")


@login_required
def show_unreaded(request, template="forum/thread_list.html"):
    u = request.user
    try:
        dt = AllVisited.objects.get(user=u).date
    except AllVisited.DoesNotExist:
        dt = datetime.datetime.now() - datetime.timedelta(FORUM_MAX_DAY_MARK)
    unreaded = Thread.objects.filter(latest_post_date__gt=dt
            ).exclude(visitedthread__user=u)
    return render_to_response(template, {
        "thread" : unreaded,
        "page": { "sitecount" : [] },
        }, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.has_perm("forum.add_post"))
def edit_post(request, thread_slug, post_id, template="forum/add_post.html"):
    t = get_object_or_404(Thread, slug=thread_slug)
    p = t.post_set.get(id=post_id)
    u = request.user
    if not t.latest_post.id == p.id or not p.author == u:
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
    if t.latest_post.id == p.id and p.author == u:
        p.delete()
    return HttpResponseRedirect("/forum/")


def quick_search(request, searchtext=None, template="forum/thread_list.html"):
    if request.GET:
        searchtext = request.GET.get("searchtext")
    pageinfo = { "sitecount" : [] }
    if not searchtext or \
            len(searchtext.replace(" ", "")) < len(searchtext.split()) * 4:
        return render_to_response(template, {
            "globalinfo": "szukanie podanej frazy może zabić bazę!",
            "page": pageinfo,
            }, context_instance=RequestContext(request))
    thread = Thread.objects.all()
    for stext in searchtext.split():
        thread = thread.filter(Q(post__text__contains=stext) | Q(title=stext))
    thread = thread.distinct()[:100]
    return render_to_response(template, {
        "thread": thread,
        "page": pageinfo,
        }, context_instance=RequestContext(request))


def advanced_search(request, template="forum/advanced_search.html"):
    if request.GET:
        pass
    f = AdvancedSearchForm()
    return render_to_response(template, {
        "form": f,
        }, context_instance=RequestContext(request))
