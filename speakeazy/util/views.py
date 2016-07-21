from django.http.response import Http404
from django.views.generic.base import View


class PostView(View):
    """
    A simple class based view for post resources.

    It may be a good idea to replace this with an actual rest framework. Preferably a lightweight framework.
    """
    http_method_names = ['post']

    def get(self):
        raise Http404()
