from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import Http404

from models import MessageBox


@login_required
def show_user_messages_box(request, template="messages/message_box.html"):
    u = request.user
    messages = MessageBox.objects.filter(receiver=u)
    return render_to_response(template, {
        "messages": messages,
        }, context_instance=RequestContext(request))

@login_required
def delete_user_message(request, id):
    message = get_object_or_404(MessageBox, id=id)
    print ":"*80
    print message.receiver
    print request.user
    print ":"*80
    if message.receiver.id is not request.user.id:
        raise Http404
    message.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'] or "/")

@login_required
def response_user_message(request, id):
    message = get_object_or_404(MessageBox, id=id)
    if message.receiver is not request.user:
        raise Http404

@login_required
def write_user_message(request):
    x = get_object_or_404(User, name="test")
