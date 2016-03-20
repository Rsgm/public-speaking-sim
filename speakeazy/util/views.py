from django.http.response import Http404
from vanilla.views import GenericView


class PostView(GenericView):
    def get(self):
        raise Http404()
