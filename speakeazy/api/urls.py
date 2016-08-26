from django.conf.urls import url, include
from rest_framework import routers
from speakeazy.api.groups.views import GroupViewSet
from speakeazy.api.views import schema_view
from speakeazy.api.groups import urls as groups

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet, base_name='group')

urlpatterns = [
    # url(r'^', schema_view),
    url(r'^', include(router.urls)),

    url(r'^', include(groups.urls(router))),
]
