from rest_framework_nested import routers
from speakeazy.api.groups import views


def urls(base_router):
    router = routers.NestedSimpleRouter(base_router, r'groups', lookup='group')

    # router.register(r'audiences', views., base_name='user')
    # router.register(r'invites', views., base_name='user')
    router.register(r'roles', views.RoleViewSet, base_name='roles')
    # router.register(r'submissions', views., base_name='user')
    # router.register(r'default-structure', views., base_name='user')
    # router.register(r'submissions', views., base_name='user')

    router.register(r'users', views.GroupMembershipViewSet, base_name='user')

    return router.urls
