import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify

from settings import FORUM_MAX_DAY_MARK
from models import Category, Thread, Post
from models import VisitedThread, AllCategoryVisit
from forms import PostForm, ThreadForm

def category_list(request, template="forum/category_list.html"):
    "Show forums list"
    category = Category.objects.all()
    return render_to_response(template, {
        "category" : category,
        }, context_instance=RequestContext(request))


def thread_list(request, category_slug, number=20, offset=0,
        template="forum/thread_list.html"):
    c = get_object_or_404(Category, slug=category_slug)
    thread = c.thread_set.all()[offset:number]
    u = request.user
    # if possible, mark threads containing new messages
    if u.is_authenticated():
        dt = datetime.datetime.now() - datetime.timedelta(FORUM_MAX_DAY_MARK)
        try:
            allcv = AllCategoryVisit.objects.get(user=u)
            dt = dt if dt > allcv.date else allcv.date
        except AllCategoryVisit.DoesNotExist:
            pass
        thread = list(thread)
        vthread = list(VisitedThread.objects.filter(user=u))
        for t in thread:
            if t.latest_post_date < dt:
                continue
            t.is_new = True
            for vt in vthread:
                if t.id == vt.thread.id and t.latest_post_date < vt.date:
                    t.is_new = False
                    break
    return render_to_response(template, {
        "category" : c,
        "thread" : thread,
        }, context_instance=RequestContext(request))

def thread(request, thread_slug, offset=0, number=20,
        template="forum/thread.html"):
    t = get_object_or_404(Thread, slug=thread_slug)
    t.view_count += 1
    t.save()
    p = t.post_set.all()[offset:number]
    f = PostForm()
    if request.user.is_authenticated():
        vt, created = VisitedThread.objects.get_or_create(
                user=request.user, thread=t)
        vt.date = datetime.datetime.now()
        vt.save()
    return render_to_response(template, {
        "thread" : t,
        "post" : p,
        "form" : f,
        }, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm("forum.add_post"))
def add_post(request, thread_slug, template="forum/add_post.html"):
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
        f = PostForm()
    return render_to_response(template, {
        "topic": t,
        "form": f,
        }, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm("forum.add_thread"))
@user_passes_test(lambda u: u.has_perm("forum.add_post"))
def add_thread(request, category_slug, template="forum/add_thread.html"):
    def get_slug(text, numb=0):
        "Create unique slug"
        if numb:
            text += "_%d" % numb
        s = slugify(text)
        if Thread.objects.filter(slug=s).count():
            return get_slug(text, numb + 1)
        return s
    u = request.user
    c = get_object_or_404(Category, slug=category_slug)
    if request.POST:
        t = Thread(author=u, category=c,
                slug=get_slug(request.POST['title']))
        tf = ThreadForm(request.POST, instance=t)
        if tf.is_valid():
            tfins = tf.save()
            p = Post(thread=tfins, author=u)
            pf = PostForm(request.POST, instance=p)
            if pf.is_valid():
                pf.save()
                return HttpResponseRedirect(c.get_absolute_url())
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
    obj, created = AllCategoryVisit.objects.get_or_create(user=u)
    if not created:
        obj.date = datetime.datetime.now()
        obj.save()
    return HttpResponseRedirect("/forum/")

@login_required
def toggle_solved(request, thread_slug):
    t = get_object_or_404(Thread, slug=thread_slug)
    if t.author == request.user:
        t.solved = not t.solved
        t.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    

@login_required
def show_unreaded(request, template="forum/thread_list.html"):
    u = request.user
    try:
        dt = AllCategoryVisit.objects.get(user=u).date
    except AllCategoryVisit.DoesNotExist:
        dt = datetime.datetime.now() - datetime.timedelta(FORUM_MAX_DAY_MARK)
    visited_th = VisitedThread.objects.filter(user=u)
    all_th = Thread.objects.filter(latest_post_date__gt=dt)
    # get unreaded posts
    unreaded = []
    for t in all_th:
        is_new = True
        for vt in visited_th:
            if t.id == vt.thread.id and t.latest_post_date < vt.date:
                is_new = False
                break
        if is_new:
            unreaded.append(t)
    return render_to_response(template, {
        "thread" : unreaded,
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
    c_ulr = t.category.get_absolute_url()
    if t.latest_post.id == p.id and p.author == u:
        p.delete()
    return HttpResponseRedirect(c_ulr)
