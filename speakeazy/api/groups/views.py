from rest_framework import viewsets

from speakeazy.api import serializers
from speakeazy.groups.models import GroupMembership, Role


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = serializers.GroupSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return self.request.user.group_set.all()


class GroupMembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = serializers.GroupMembershipSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return GroupMembership.objects.filter(group__in=self.request.user.group_set.all())


class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows roles to be viewed or edited.
    """
    serializer_class = serializers.Role
    lookup_field = 'pk'

    def get_queryset(self):
        return Role.objects.filter(group__in=self.request.user.group_set.all())
