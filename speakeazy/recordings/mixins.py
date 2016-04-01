from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from speakeazy.groups.models import Submission, SUBMISSION_IN_PROGRESS, SUBMISSION_READY
from speakeazy.groups.permissions import EVALUATE_SUBMISSION
from speakeazy.recordings.models import SharedUser, Recording, SharedLink
from django.utils import timezone

OWNER = 'owner'
GRADER = 'grader'
SHARED_USER = 'shared-user'
SHARED_GROUP = 'shared-group'
SHARED_LINK = 'link'


def not_found():
    raise Http404()


class RecordingAuthorizationMixin(object):
    """
    View mixin which verifies that a user has access to view a recording, comment, or evaluate.
    """

    recording = None
    authorization = {}

    # these may be overridden
    allowed = [OWNER, GRADER, SHARED_USER, SHARED_LINK]
    owner_only = None

    def dispatch(self, request, *args, **kwargs):
        auth_type = kwargs['type']
        self.authorization['type'] = auth_type
        self.authorization['key'] = kwargs['key']

        if auth_type not in self.allowed:
            not_found()

        elif auth_type == OWNER:
            self.owner(request, *args, **kwargs)

        elif auth_type == GRADER:
            self.grader(request, *args, **kwargs)

        elif auth_type == SHARED_USER:
            self.shared_user(request, *args, **kwargs)

        elif auth_type == SHARED_LINK:
            self.shared_link(request, *args, **kwargs)

        return super(RecordingAuthorizationMixin, self).dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def owner(self, request, *args, **kwargs):
        queryset = Recording.objects.filter(pk=kwargs['key'], project__user=request.user) \
            .select_related('project__user')

        self.recording = get_object_or_404(queryset)
        self.authorization['comments'] = True
        self.authorization['evaluations'] = True

    @method_decorator(login_required)
    def grader(self, request, *args, **kwargs):
        queryset = Submission.objects.filter(pk=kwargs['key']) \
            .select_related('group', 'recording', 'group_visibility')

        submission = get_object_or_404(queryset)

        # check submission state, todo: clean this up a  bit
        if submission.state == SUBMISSION_IN_PROGRESS and submission.grader == request.user:
            pass
        elif submission.state == SUBMISSION_READY:
            submission.state = SUBMISSION_IN_PROGRESS
            submission.grader = request.user
            submission.save()
        else:
            not_found()

        # check permissions
        permissions = request.user.groupmembership_set.filter(group=submission.group) \
            .values_list('authorizations__permissions__name', flat=True)
        if EVALUATE_SUBMISSION not in permissions:
            not_found()

        self.recording = submission.recording
        self.authorization['comments'] = True
        self.authorization['evaluations'] = True

    @method_decorator(login_required)
    def shared_user(self, request, *args, **kwargs):
        queryset = SharedUser.objects.filter(pk=kwargs['key'], user=request.user) \
            .select_related('recording', 'user', 'recording__comments', 'recording__evaluations')

        shared_user = get_object_or_404(queryset)

        self.recording = shared_user.recording
        self.authorization['comments'] = shared_user.comments
        self.authorization['evaluations'] = shared_user.evaluations

    # No login required
    def shared_link(self, request, *args, **kwargs):
        queryset = SharedLink.objects.filter(uuid=kwargs['key']) \
            .select_related('recording', 'recording__comments', 'recording__evaluations')

        shared_link = get_object_or_404(queryset)

        # check if authorized
        if shared_link.login_required and not request.user.is_authenticated:
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
