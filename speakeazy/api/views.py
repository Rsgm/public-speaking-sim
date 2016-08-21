from rest_framework import viewsets

from speakeazy.api.serializers import GroupSerializer, GroupMembershipSerializer
from speakeazy.groups.models import GroupMembership


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = GroupSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return self.request.user.group_set.all()


class GroupMembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = GroupMembershipSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return GroupMembership.objects.filter(group__in=self.request.user.group_set.all())
