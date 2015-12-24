from braces.views import LoginRequiredMixin
from vanilla.views import TemplateView, FormView


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'speakeazy/join/home.html'


class Token(LoginRequiredMixin, FormView):
    template_name = 'speakeazy/join/home.html'


class Name(LoginRequiredMixin, FormView):
    template_name = 'speakeazy/join/home.html'


class Request(LoginRequiredMixin, FormView):
    template_name = 'speakeazy/join/home.html'
