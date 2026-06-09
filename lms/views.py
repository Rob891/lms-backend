from django.shortcuts import render
from rest_framework import viewsets,generics
from rest_framework.exceptions import NotAuthenticated,PermissionDenied
from .models import Profile, Course, Chapter,Enrollment
from .serializers import(ProfileSerializer,CourseSerializer,ChapterSerializer,EnrollmentSerializer,RegisterSerializer)
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login,logout

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.middleware.csrf import get_token
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from django.contrib.auth import logout

# Create your views here.

class CsrfTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({"csrfToken": get_token(request)})
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class= ProfileSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_authenticated:
            raise NotAuthenticated("You must be logged in to create a course")

        profile = Profile.objects.get(user=user)

        if profile.role != "instructor":
            raise PermissionDenied("Only instructors can create courses.")

        serializer.save(instructor=user)
class MyCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            raise NotAuthenticated("You must be logged in.")

        profile = Profile.objects.get(user=user)

        if profile.role == "instructor":
            return Course.objects.filter(instructor=user)

        if profile.role == "student":
            enrolled_courses = Enrollment.objects.filter(
                student=user
            ).values_list("course", flat=True)

            return Course.objects.filter(id__in=enrolled_courses)

        return Course.objects.none()


class ChapterViewSet(viewsets.ModelViewSet):
    queryset= Chapter.objects.all()
    serializer_class=ChapterSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            profile = Profile.objects.get(user=user)

            if profile.role == "instructor":
                return Chapter.objects.filter(course__instructor=user)
            if profile.role == "student":
                enrolled_courses =Enrollment.objects.filter(student=user).values_list("course", flat=True)
                return Chapter.objects.filter(course__in = enrolled_courses,
                    is_public =True)
        return Chapter.objects.none()    



    def perform_create(self, serializer):
        user = self.request.user
        
        if not user.is_authenticated:
            raise NotAuthenticated("Must be logged in to create chapter.")
        
        profile = Profile.objects.get(user=user)
        if profile.role != "instructor":
            raise PermissionDenied("Only instructors can create chapters.")
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

class MeView(APIView):
    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            raise NotAuthenticated("You must be logged in.")

        profile = Profile.objects.get(user=user)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": profile.role,
        })
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        user = authenticate(
            request,
            username=request.data.get("username"),
            password=request.data.get("password")
        )

        if user is None:
            raise PermissionDenied("Invalid username or password.")

        login(request, user)

        request.session.save()

        profile = Profile.objects.get(user=user)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": profile.role,
        })
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})

