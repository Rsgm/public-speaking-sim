from django.conf.urls import url, include
from rest_framework import routers

from speakeazy.api import views

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet, base_name='group')
router.register(r'groups/admin/users', views.GroupMembershipViewSet, base_name='user')
# router.register(r'groups/admin/invites', views., base_name='user')

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^', include(router.urls)),
]
