from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"items", views.ItemViewSet)
router.register(r"reviews", views.ReviewViewSet)
# router.register(r"users", views.UserViewSet)
# router.register(r"groups", views.GroupViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
