# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
#from django.contrib.auth.models import User
from django.http import Http404

from models import MessageBox
from forms import MessageBoxForm


@login_required
def received_user_messages(request, template="messages/message_box.html"):
    messages = MessageBox.objects.filter(receiver=request.user)
    return render_to_response(template, {
        "messages": messages,
        }, context_instance=RequestContext(request))

@login_required
def sended_user_messages(request, template="messages/message_box.html"):
    messages = MessageBox.objects.filter(sender=request.user)
    return render_to_response(template, {
        "messages": messages,
        }, context_instance=RequestContext(request))

@login_required
def delete_user_message(request, id):
    message = get_object_or_404(MessageBox, id=id)
    if message.receiver.id is not request.user.id:
        raise Http404
    message.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'] or "/")

@login_required
def response_user_message(request, id):
    message = get_object_or_404(MessageBox, id=id)
    # disallow to response to other users message
    if message.receiver.id is not request.user.id:
        raise Http404
    text = "> " + str(message.sender) + ":\n>\n> " + \
           message.text.replace("\n", "\n> ") + "\n\n"
    form = MessageBoxForm({'text': text, 'receiver': message.sender.id })
    return write_user_message(request, form)

@login_required
def write_user_message(request, form=None, template="messages/write.html"):
    if request.POST:
        m = MessageBox(sender=request.user)
        form = MessageBoxForm(request.POST, instance=m)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/messages/sended/")
    elif not form:
        form = MessageBoxForm()
    return render_to_response(template, {
        "form": form,
        }, context_instance=RequestContext(request))

