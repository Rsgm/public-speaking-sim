from rest_framework import serializers
from speakeazy.groups.models import Group, GroupMembership
from speakeazy.users.models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'name', 'description', 'slug')


class GroupMembershipSerializer(serializers.ModelSerializer):
    # roles = serializers.HyperlinkedRelatedField(view_name='group-detail', lookup_field='username', read_only=True)

    class Meta:
        model = GroupMembership
        fields = ('group', 'user', 'roles', 'created_time',)
