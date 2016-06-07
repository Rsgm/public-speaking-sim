from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from speakeazy.groups.mixins import GroupMixin
from speakeazy.groups.permissions import VIEW_SUBMISSION, DELETE_SUBMISSION, \
    EVALUATE_SUBMISSION, LIST_SUBMISSION
from speakeazy.groups.models import Submission
from speakeazy.recordings.models import EvaluationType, Evaluation
from vanilla.model_views import DetailView, ListView, DeleteView
from vanilla.views import TemplateView


class Dashboard(LoginRequiredMixin, GroupMixin, TemplateView):
    # group_permission =
    pass


class UserRoleOverview(LoginRequiredMixin, GroupMixin, TemplateView):
    # group_permission =
    pass
