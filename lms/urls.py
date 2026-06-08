from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    ProfileViewSet,CourseViewSet,ChapterViewSet,EnrollmentViewSet,RegisterView
)
router = DefaultRouter()

router.register(r"profiles", ProfileViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"chapters", ChapterViewSet)
router.register(r"enrollments", EnrollmentViewSet)

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
]
urlpatterns += router.urls