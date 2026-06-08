from rest_framework  import serializers
from django.contrib.auth.models import User
from .models import Profile, Course,Chapter,Enrollment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email"]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ["id","user","role"]

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    class Meta:
        model= Course
        fields = ["id","instructor","title","description"]

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields =     ["id","course","title","content","is_public"]

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id","student","course"]

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id","username","email","password","role"]
    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        user = User.objects.create_user(
            username=validated_data["username"],
            email= validated_data.get("email",""),
            password= password

        )
        Profile.objects.create(user=user, role=role)
        return user

