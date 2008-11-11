# -*- coding: utf-8 -*-

import time
import datetime

from settings import FORUM_MAX_DAY_MARK
from models import Forum, Topic, TopicVisit
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def set_all_readed(request):
    "Set all topics as readed"
    t = time.gmtime()
    user = request.user
    # clear database for that user
    TopicVisit.filter(user__eq=user.username).delete()
    # add new 'read' sentry for each forum
    for topic in Topic.filter(date__gt=t[:3]):
        # TODO - one sql commit
        tview = TopicVisit(user=user, topic=topic)
        tview.save()

@login_required
def set_forum_readed(request, forum_id=None, forum_slug=None):
    if forum_id:
        forum = get_object_or_404(Forum, id=forum_id)
    else:
        forum = get_object_or_404(Forum, slug=forum_slug)
    user = request.user
    t = time.gmtime()
    for topic in Topic.filter(date__gt=delay_date()):
        pass

@login_required
def set_topic_readed(request, topic):
    if topic_id:
        topic = get_object_or_404(Topic, id=topic_id)
    else:
        topic = get_object_or_404(Topic, slug=topic_slug)
    user = request.user
    tview = TopicVisit(user=user, topic=topic)
    tview.save()


def delay_date():
    return datetime.datetime(*time.gmtime()[:6]) - \
            datetime.timedelta(FORUM_MAX_DAY_MARK)
