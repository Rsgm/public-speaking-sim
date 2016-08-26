from rest_framework import serializers
from speakeazy.groups.models import Group, GroupMembership, Role


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'description', 'slug')
        read_only_fields = ('slug',)


class GroupMembershipSerializer(serializers.ModelSerializer):
    permissions = serializers.StringRelatedField()

    # group = serializers.HyperlinkedRelatedField(view_name='group-detail', lookup_field='slug', read_only=True)

    class Meta:
        model = GroupMembership
        fields = ('group', 'user', 'roles', 'created_time')
        read_only_fields = ('group', 'user')


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.StringRelatedField(many=True)
    # group = serializers.HyperlinkedRelatedField(view_name='group-detail', lookup_field='slug', read_only=True)

    class Meta:
        model = Role
        fields = ('name', 'group', 'permissions')
        read_only_fields = ('group',)
