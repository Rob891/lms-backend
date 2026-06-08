from django.shortcuts import render
from rest_framework import viewsets,generics
from rest_framework.exceptions import NotAuthenticated,PermissionDenied
from .models import Profile, Course, Chapter,Enrollment
from .serializers import(ProfileSerializer,CourseSerializer,ChapterSerializer,EnrollmentSerializer,RegisterSerializer)
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


# Create your views here.

class ProfileViewSet(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class= ProfileSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset= Course.objects.all()
    serializer_class= CourseSerializer
    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("You must be logged in to create a course")
        
        profile = Profile.objects.get(user=user)

        if profile.role != "instructor":
            raise PermissionDenied("Only instructors can create courses.")
        serializer.save(instructor=user)


class ChapterViewSet(viewsets.ModelViewSet):
    queryset= Chapter.objects.all()
    serializer_class=ChapterSerializer
    def perform_create(self, serializer):
        user = self.request.user
        
        if not user.is_authenticated:
            raise NotAuthenticated("Must be logged in to create chapter.")
        
        profile = Profile.objects.get(user=user)
        if profile.role != "instructor":
            raise PermissionDenied("Only instrcutors can create chapters.")
        serializer.save()


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    def perform_create(self, serializer):
        user = self.request.user
        
        if not user.is_authenticated:
            raise NotAuthenticated("must be logged in to join a course")
        profile = Profile.objects.get(user=user)
        if profile.role != "student":
            raise PermissionDenied("must be student to enroll")
        serializer.save(student = user)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

