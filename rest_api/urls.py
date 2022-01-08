from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_api import views


router = DefaultRouter()
router.register('UserProfile', views.UserProfileViewSet)

urlpatterns = [

    path('', include(router.urls)),
    path('login', views.UserLoginApiView.as_view()),

]
