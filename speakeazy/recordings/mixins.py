from django.http.response import Http404
from django.shortcuts import get_object_or_404
from speakeazy.groups.models import Submission
from speakeazy.groups.permissions import EVALUATE_SUBMISSION
from speakeazy.recordings.models import SharedUser, Recording, SharedLink
from django.utils import timezone

OWNER = 'owner'
GRADER = 'grader'
SHARED_USER = 'shared-user'
SHARED_GROUP = 'shared-group'
SHARED_LINK = 'link'

ALLOWED = {OWNER, GRADER, SHARED_USER, SHARED_LINK}


def not_found():
    raise Http404()


class RecordingMixin(object):
    """
    View mixin which verifies that a user has access to view a recording, comment, or evaluate.

    Needs login required mixin on the view
    """

    # these may be overridden
    allowed = ALLOWED

    recording = None
    submission = None
    authorization = {}

    owner_only = None

    def dispatch(self, request, *args, **kwargs):
        auth_type = kwargs['type']
        self.authorization['type'] = auth_type
        self.authorization['key'] = kwargs['key']

        logged_in = request.user.is_authenticated()

        if auth_type not in self.allowed:
            not_found()

        elif auth_type == OWNER and logged_in:
            self.owner(request, *args, **kwargs)

        elif auth_type == GRADER and logged_in:
            self.grader(request, *args, **kwargs)

        elif auth_type == SHARED_USER and logged_in:
            self.shared_user(request, *args, **kwargs)

        elif auth_type == SHARED_LINK:
            self.shared_link(request, *args, **kwargs)

        else:
            not_found()

        return super(RecordingMixin, self).dispatch(request, *args, **kwargs)

    def owner(self, request, *args, **kwargs):
        queryset = Recording.objects.filter(pk=kwargs['key'], project__user=request.user) \
            .select_related('project__user')

        self.recording = get_object_or_404(queryset)
        self.authorization['comments'] = True
        self.authorization['evaluations'] = True

    def grader(self, request, *args, **kwargs):
        queryset = Submission.objects.filter(pk=kwargs['key']) \
            .select_related('group', 'recording', 'recording__project', 'recording__project__user')

        self.submission = get_object_or_404(queryset)

        # ignore this for now
        # # check submission availability
        # if submission.grader == request.user and not submission.finished:
        #     pass
        # elif submission.grader is None:
        #     submission.grader = request.user
        #     submission.save()
        # else:
        #     not_found()

        # check permissions
        permissions = request.user.groupmembership_set.filter(group=self.submission.group) \
            .values_list('roles__permissions__name', flat=True)
        if EVALUATE_SUBMISSION not in permissions:
            not_found()

        self.recording = self.submission.recording
        self.authorization['comments'] = True
        self.authorization['evaluations'] = True

    def shared_user(self, request, *args, **kwargs):
        queryset = SharedUser.objects.filter(pk=kwargs['key'], user=request.user) \
            .select_related('recording', 'user', 'recording__comments', 'recording__evaluations')

        shared_user = get_object_or_404(queryset)

        self.recording = shared_user.recording
        self.authorization['comments'] = shared_user.comments
        self.authorization['evaluations'] = shared_user.evaluations

    def shared_link(self, request, *args, **kwargs):
        queryset = SharedLink.objects.filter(uuid=kwargs['key']) \
            .select_related('recording', 'recording__comments', 'recording__evaluations')

        shared_link = get_object_or_404(queryset)

        # check if authorized
        if shared_link.login_required and not request.user.is_authenticated():
            not_found()
        if shared_link.uses == 0:
            not_found()
        if timezone.now() > shared_link.expires:
            not_found()

        if shared_link.uses > 0:
            shared_link.uses -= 1
            shared_link.save()

        self.recording = shared_link.recording
        self.authorization['comments'] = shared_link.comments
        self.authorization['evaluations'] = shared_link.evaluations
