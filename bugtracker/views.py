from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from models import Bug, BugComment
from forms import BugForm, BugCommentForm

def bug_reported(request, template="bugtracker/list.html"):
    "List retent bug reports"
    b = Bug.objects.exclude(closed=True)
    return render_to_response(template, {
        "buglist": b,
        }, context_instance=RequestContext(request))

def bug_closed(request, template="bugtracker/list.html"):
    b = Bug.objects.filter(closed=True)
    return render_to_response(template, {
        "buglist": b,
        }, context_instance=RequestContext(request))

def bug_show(request, bug_id, template="bugtracker/details.html"):
    b = get_object_or_404(Bug, id=int(bug_id))
    c = BugComment.objects.filter(bug=b)
    f = BugCommentForm()
    return render_to_response(template, {
        "bug": b,
        "comments": c,
        "form": f,
        }, context_instance=RequestContext(request))

@login_required
def bug_comment(request, bug_id, template="bugtracker/details.html"):
    b = get_object_or_404(Bug, id=int(bug_id))
    if request.POST:
        bc = BugComment(bug=b, author=request.user)
        f = BugCommentForm(request.POST, instance=bc)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(b.get_absolute_url() or "/")
    else:
        f = BugCommentForm()
    return render_to_response(template, {
        "buglist": b,
        "form": f,
        }, context_instance=RequestContext(request))


@login_required
def bug_report(request, template="bugtracker/report.html"):
    if request.POST:
        b = Bug(reported_by=request.user)
        f = BugForm(request.POST, instance=b)
        if f.is_valid():
            b = f.save()
            return HttpResponseRedirect(b.get_absolute_url() or "/")
    else:
        f = BugForm()
    return render_to_response(template, {
        "form": f,
        }, context_instance=RequestContext(request))

