from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers.school_admin import (
    UserSerializer, ClassroomSerializer, SubjectSerializer, ClassroomSubjectSerializer
)
from ..models import User
from classrooms.models import Classroom
from subjects.models import Subject, ClassroomSubject


class SchoolAdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(school=self.request.user.school)


class SchoolAdminClassroomListView(generics.ListAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Classroom.objects.filter(school=self.request.user.school)


class SchoolAdminSubjectListView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subject.objects.filter(school=self.request.user.school)


class SchoolAdminClassroomSubjectListView(generics.ListAPIView):
    serializer_class = ClassroomSubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ClassroomSubject.objects.filter(classroom__school=self.request.user.school)
