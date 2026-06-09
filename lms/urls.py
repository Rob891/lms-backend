from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    ProfileViewSet,CourseViewSet,ChapterViewSet,EnrollmentViewSet,RegisterView
)
from .views import MyCoursesView
from .views import MeView
from .views import LoginView
from .views import CsrfTokenView
from .views import LogoutView
router = DefaultRouter()

router.register(r"profiles", ProfileViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"chapters", ChapterViewSet)
router.register(r"enrollments", EnrollmentViewSet)

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("my-courses/", MyCoursesView.as_view(), name="my-courses"),
    path("me/", MeView.as_view()),
    path("login/", LoginView.as_view()),
    path("csrf/", CsrfTokenView.as_view()),
    path("logout/", LogoutView.as_view()),

]
urlpatterns += router.urls