from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import StaticPage


def show_static_page(request, slug, template="staticpages/base.html"):
    page = get_object_or_404(StaticPage, slug=slug)
    return render_to_response(template, {
        "page": page,
        }, context_instance=RequestContext(request))
