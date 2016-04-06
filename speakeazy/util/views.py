from django.http.response import Http404
from vanilla.views import GenericView


class PostView(GenericView):
    http_method_names = ['post']

    def get(self):
        raise Http404()
