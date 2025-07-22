from rest_framework import generics, permissions
from .models import Teacher
from .serializers import TeacherSerializer


class TeacherListCreateView(generics.ListCreateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Teacher.objects.filter(user__school=self.request.user.school)

    def get_serializer_context(self):
        return {'request': self.request}


class TeacherRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Teacher.objects.filter(user__school=self.request.user.school)

    def get_serializer_context(self):
        return {'request': self.request}
